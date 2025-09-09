import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
import polars as pl
from polars import col as c

from app import app, db
from app.models import Shift, Game, Event, SplitShift
from . import cleaning

def get_shift(id: int):
    return db.session.get(Shift, id)

def get_shift_events(shift: Shift) -> list[tuple]:
    stmt = (sa.select(Event.period, Event.timeInPeriodSec, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.typeCode, Event.xCoord,  Event.homeTeamDefendingSide, Event.eventOwnerTeamID, Game.homeTeamID, Event.xg)
            .join(Event.game)
            .where(Event.gameID == shift.gameID,
                   Event.period == shift.period,
                   Event.timeInPeriodSec >= shift.startTimeSec,
                   Event.timeInPeriodSec <= shift.endTimeSec)
            .order_by(Event.timeInPeriodSec, Event.sortOrder)
    )
    return db.session.execute(stmt).all()

def calculate_shift_data(event_data: pl.DataFrame) -> pl.DataFrame:
    q = (
        event_data.lazy()
        .group_by('teamID', 'playerID', 'gameID', 'shiftID', 'strengthState', 'period', 'split')
        .agg(
            ((c('typeCode') == 505) & c('forPlayer')).sum().alias('goalsFor'),
            ((c('typeCode') == 505) & c('forPlayer').not_()).sum().alias('goalsAgainst'),
            ((c('typeCode').is_in([505,506]) & c('forPlayer'))).sum().alias('sogFor'),
            ((c('typeCode').is_in([505,506]) & c('forPlayer').not_())).sum().alias('sogAgainst'),
            ((c('typeCode').is_in([505,506,507]) & c('forPlayer'))).sum().alias('fenwickFor'),
            ((c('typeCode').is_in([505,506,507]) & c('forPlayer').not_())).sum().alias('fenwickAgainst'),
            ((c('typeCode').is_in([505,506,507,508]) & c('forPlayer'))).sum().alias('corsiFor'),
            ((c('typeCode').is_in([505,506,507,508]) & c('forPlayer').not_())).sum().alias('corsiAgainst'),
            c('xg').filter(c('forPlayer')).sum().alias('xgFor'),
            c('xg').filter(c('forPlayer').not_()).sum().alias('xgAgainst'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'O')).sum().alias('oZoneStarts'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'D')).sum().alias('dZoneStarts'),
            ((c('typeCode') == 502) & (c('faceoffZone') == 'N')).sum().alias('nZoneStarts'),
            c('timeInPeriodSec').first().alias('startTimeSec'),
            c('timeNextEvent').last().fill_null(c('timeInPeriodSec').last()).alias('endTimeSec')
        )
        .with_columns(splitDuration = c('endTimeSec') - c('startTimeSec'))
        .unnest('strengthState')
        .filter(c('splitDuration') > 0)
    )
    return q.collect()

def concat_shift_events(*shifts: Shift):
    all_events = []
    for shift in shifts:
        events = get_shift_events(shift)
        shift_events = cleaning.clean_shift_events(shift, events)
        all_events.append(shift_events)

    all_events_df: pl.DataFrame = pl.concat(all_events)
    return all_events_df.pipe(cleaning.add_faceoff_zone).pipe(cleaning.add_strengths)

def get_game_shifts(gameID: int) -> list[Shift]:
    stmt = sa.select(Shift).where(Shift.gameID == gameID)
    return db.session.execute(stmt).scalars().all()

def get_season_shifts(season: int) -> list[Shift]:
    gameIDs = db.session.execute(sa.select(Game.id).where(Game.season == season)).scalars().all()
    stmt = sa.select(Shift).where(Shift.gameID.in_(gameIDs))
    return db.session.execute(stmt).scalars().all()

def insert_split_shifts(data: pl.DataFrame):
    dicts = data.rows(named=True)
    stmt = sqlite_upsert(SplitShift).values(dicts)
    stmt = stmt.on_conflict_do_update(
        index_elements=[SplitShift.shiftID, SplitShift.split],
        set_ = {
            SplitShift.teamID: stmt.excluded.teamID,
            SplitShift.playerID: stmt.excluded.playerID,
            SplitShift.gameID: stmt.excluded.gameID,
            SplitShift.period: stmt.excluded.period,
            SplitShift.startTimeSec: stmt.excluded.startTimeSec,
            SplitShift.endTimeSec: stmt.excluded.endTimeSec,
            SplitShift.splitDuration: stmt.excluded.splitDuration,
            SplitShift.attackingSkaters: stmt.excluded.attackingSkaters,
            SplitShift.defendingSkaters: stmt.excluded.defendingSkaters,
            SplitShift.attackingGoalie: stmt.excluded.attackingGoalie,
            SplitShift.defendingGoalie: stmt.excluded.defendingGoalie,
            SplitShift.goalsFor: stmt.excluded.goalsFor,
            SplitShift.goalsAgainst: stmt.excluded.goalsAgainst,
            SplitShift.sogFor: stmt.excluded.sogFor,
            SplitShift.sogAgainst: stmt.excluded.sogAgainst,
            SplitShift.fenwickFor: stmt.excluded.fenwickFor,
            SplitShift.fenwickAgainst: stmt.excluded.fenwickAgainst,
            SplitShift.corsiFor: stmt.excluded.corsiFor,
            SplitShift.corsiAgainst: stmt.excluded.corsiAgainst,
            SplitShift.xgFor: stmt.excluded.xgFor,
            SplitShift.xgAgainst: stmt.excluded.xgAgainst,
            SplitShift.dZoneStarts: stmt.excluded.dZoneStarts,
            SplitShift.nZoneStarts: stmt.excluded.nZoneStarts,
            SplitShift.oZoneStarts: stmt.excluded.oZoneStarts,
        }
    )
    db.session.execute(stmt)
    db.session.commit()

if __name__ == "__main__":
    app.app_context().push()

    # shift = get_shift(7233472)
    # with pl.Config(tbl_cols=-1):
    #     print(cleaning.clean_shift_events(shift, get_shift_events(shift)))

    gameIDs = db.session.execute(sa.select(Game.id).where(Game.season == 20222023)).scalars().all()
    counter = 0
    num_games = len(gameIDs)
    for gameID in gameIDs:
        shifts = get_game_shifts(gameID)
        events = concat_shift_events(*shifts)
        splitshifts = calculate_shift_data(events)
        insert_split_shifts(splitshifts)
        counter += 1
        app.logger.info(f'Inserted Split Shifts for Game {gameID} ({counter}/{num_games})')