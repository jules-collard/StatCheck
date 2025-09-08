import sqlalchemy as sa
import polars as pl
import polars.selectors as cs
from polars import col as c

from app import app, db
from app.models import Shift, Game, Event
from .cleaning import add_faceoff_zone, add_strengths

schema = {
    'timeInPeriodSec': pl.Int16,
    'awayGoalie': pl.Int8,
    'awaySkaters': pl.Int8,
    'homeGoalie': pl.Int8,
    'homeSkaters': pl.Int8,
    'typeCode': pl.Int16,
    'xCoord': pl.Float32,
    'homeTeamDefendingSide': pl.Enum(['left', 'right']),
    'eventOwnerTeamID': pl.Int8,
    'homeTeamID': pl.Int8,
    'xg': pl.Float64
}

def get_shift_start_event(startTime: int, awayGoalie, awaySkaters, homeGoalie, homeSkaters):
    return {
        'timeInPeriodSec': startTime,
        'awayGoalie': awayGoalie,
        'awaySkaters': awaySkaters,
        'homeGoalie': homeGoalie,
        'homeSkaters': homeSkaters,
        'typeCode': 600,
        'xCoord': None,
        'homeTeamDefendingSide': None,
        'eventOwnerTeamID': None,
        'homeTeamID': None,
        'xg': None,
    }

def get_shift_end_event(endTime: int, awayGoalie, awaySkaters, homeGoalie, homeSkaters):
    return {
        'timeInPeriodSec': endTime,
        'awayGoalie': awayGoalie,
        'awaySkaters': awaySkaters,
        'homeGoalie': homeGoalie,
        'homeSkaters': homeSkaters,
        'typeCode': 600,
        'xCoord': None,
        'homeTeamDefendingSide': None,
        'eventOwnerTeamID': None,
        'homeTeamID': None,
        'xg': None,
    }

def get_shift(id: int):
    return db.session.get(Shift, id)

def get_shift_events(shift: Shift):
    stmt = (sa.select(Event.timeInPeriodSec, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.typeCode, Event.xCoord,  Event.homeTeamDefendingSide, Event.eventOwnerTeamID, Game.homeTeamID, Event.xg)
            .join(Event.game)
            .where(Event.gameID == shift.gameID,
                   Event.period == shift.period,
                   Event.timeInPeriodSec >= shift.startTimeSec,
                   Event.timeInPeriodSec <= shift.endTimeSec)
            .order_by(Event.timeInPeriodSec, Event.sortOrder)
    )
    data = db.session.execute(stmt).all()
    
    data = (pl.DataFrame(data, schema=schema, orient='row')
            .filter(((c('typeCode') == 502) & (c('timeInPeriodSec') == shift.endTimeSec)).not_(), # remove faceoff at end of shift
                    ((c('typeCode') == 516) & (c('timeInPeriodSec') == shift.startTimeSec)).not_())) # Remove stoppage at start of shift
    
    if len(data) == 0:
        first_strength_state = (1,5,1,5)
        last_strength_state = (1,5,1,5)
    else:
        first_strength_state = data.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(0)
        last_strength_state = data.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(-1)
    
    start_event = get_shift_start_event(shift.startTimeSec, *first_strength_state)
    end_event = get_shift_end_event(shift.endTimeSec, *last_strength_state)

    data = pl.concat([pl.DataFrame(start_event, schema=schema), data, pl.DataFrame(end_event, schema=schema)])
    
    data = (data.lazy()
            .with_columns(teamID = shift.teamID,
                            playerID = shift.playerID,
                            shiftID = shift.id,
                            forPlayer = c('eventOwnerTeamID') == shift.teamID,
                            timeNextEvent = c('timeInPeriodSec').shift(-1)))
    return data.collect()

def calculate_shift_data(shift_data: pl.DataFrame):
    q = (
        shift_data.lazy()
        .group_by('teamID', 'playerID', 'shiftID', 'strengthState', 'split')
        .agg(
            ((c('typeCode') == 505) & c('forPlayer')).sum().alias('goalsFor'),
            ((c('typeCode') == 505) & c('forPlayer').not_()).sum().alias('goalsAgainst'),
            ((c('typeCode').is_in([505,506,507]) & c('forPlayer'))).sum().alias('fenwickFor'),
            ((c('typeCode').is_in([505,506,507]) & c('forPlayer').not_())).sum().alias('fenwickAgainst'),
            ((c('typeCode').is_in([505,506,507,508]) & c('forPlayer'))).sum().alias('corsiFor'),
            ((c('typeCode').is_in([505,506,507,508]) & c('forPlayer').not_())).sum().alias('corsiAgainst'),
            c('xg').filter(c('forPlayer')).sum().alias('xgFor'),
            c('xg').filter(c('forPlayer').not_()).sum().alias('xgAgainst'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'O')).sum().alias('oZoneStarts'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'D')).sum().alias('dZoneStarts'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'N')).sum().alias('nZoneStarts'),
            (c('timeNextEvent').last() - c('timeInPeriodSec').first()).fill_null(c('timeInPeriodSec').last() - c('timeInPeriodSec').first()).alias('splitLength')
        )
        .unnest('strengthState')
    )
    return q.collect()

def concat_shift_events(*shifts: Shift):
    all_events = []
    for shift in shifts:
        shift_events = get_shift_events(shift)
        if shift_events is not None:
            all_events.append(shift_events)

    all_events_df: pl.DataFrame = pl.concat(all_events)
    return all_events_df.pipe(add_faceoff_zone).pipe(add_strengths)

def get_game_shifts(gameID: int) -> list[Shift]:
    stmt = sa.select(Shift).where(Shift.gameID == gameID)
    return db.session.execute(stmt).scalars()

if __name__ == "__main__":
    app.app_context().push()
    shifts = get_game_shifts(2024190006)
    events = concat_shift_events(*shifts)
    data = calculate_shift_data(events)
    with pl.Config(tbl_cols=-1):
        print(data.sort('shiftID'))