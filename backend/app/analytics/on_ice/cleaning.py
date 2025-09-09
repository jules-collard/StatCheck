import polars as pl
import polars.selectors as cs
from polars import col as c

from app.models import Shift

schema = {
    'period': pl.Int8,
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

def get_shift_start_event(period: int, startTime: int, awayGoalie, awaySkaters, homeGoalie, homeSkaters):
    return {
        'period': period,
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

def get_shift_end_event(period: int, endTime: int, awayGoalie, awaySkaters, homeGoalie, homeSkaters):
    return {
        'period': period,
        'timeInPeriodSec': endTime,
        'awayGoalie': awayGoalie,
        'awaySkaters': awaySkaters,
        'homeGoalie': homeGoalie,
        'homeSkaters': homeSkaters,
        'typeCode': 601,
        'xCoord': None,
        'homeTeamDefendingSide': None,
        'eventOwnerTeamID': None,
        'homeTeamID': None,
        'xg': None,
    }

def add_faceoff_zone(data: pl.DataFrame):
    q = data.lazy().with_columns(
        faceoffZone = pl.when(c('homeTeamID') == c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') > 25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') < -25)))
                    .then(pl.lit('D'))
                    .when(c('homeTeamID') == c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') < -25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') > 25)))
                    .then(pl.lit('O'))
                    .when(c('homeTeamID') != c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') < -25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') > 25)))
                    .then(pl.lit('D'))
                    .when(c('homeTeamID') != c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') > 25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') < -25)))
                    .then(pl.lit('O'))
                    .when(c('homeTeamDefendingSide').is_null() | c('xCoord').is_null() | (c('typeCode') != 502))
                    .then(None)
                    .otherwise(pl.lit('N'))
                    .cast(pl.Enum(['D', 'N', 'O']))
    )
    return q.collect()

def add_strengths(data: pl.DataFrame):
    return (data.lazy()
            .with_columns(attackingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('homeSkaters')).otherwise(c('awaySkaters')),
                          defendingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('awaySkaters')).otherwise(c('homeSkaters')),
                          attackingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('homeGoalie')).otherwise(c('awayGoalie')),
                          defendingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('awayGoalie')).otherwise(c('homeGoalie')))
            .with_columns(manAdvantage = c('attackingSkaters') - c('defendingSkaters'),
                          strengthState = pl.struct(['attackingSkaters', 'defendingSkaters', 'attackingGoalie', 'defendingGoalie']))
            .with_columns(split = c('manAdvantage').rle_id().over('shiftID'))
            .drop('xCoord', 'homeTeamDefendingSide', cs.contains('Goalie', 'Skaters'))
            .collect())

def clean_shift_events(shift: Shift, events: list[tuple]):
    data = (pl.DataFrame(events, schema=schema, orient='row')
            .filter(((c('typeCode') == 502) & (c('timeInPeriodSec') == shift.endTimeSec)).not_(), # remove faceoff at end of shift
                    ((c('typeCode') == 516) & (c('timeInPeriodSec') == shift.startTimeSec)).not_())
            .drop_nulls(subset=['awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters'])) # Remove stoppage at start of shift
    
    if len(data) == 0:
        first_strength_state = (1,5,1,5)
        last_strength_state = (1,5,1,5)
    else:
        first_strength_state = data.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(0)
        last_strength_state = data.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(-1)
    
    start_event = get_shift_start_event(shift.period, shift.startTimeSec, *first_strength_state)
    end_event = get_shift_end_event(shift.period, shift.endTimeSec, *last_strength_state)

    data = pl.concat([pl.DataFrame(start_event, schema=schema), data, pl.DataFrame(end_event, schema=schema)])
    
    data = (data.lazy()
            .with_columns(teamID = shift.teamID,
                          playerID = shift.playerID,
                          gameID = shift.gameID,
                          shiftID = shift.id,
                          forPlayer = c('eventOwnerTeamID') == shift.teamID,
                          timeNextEvent = c('timeInPeriodSec').shift(-1)))
    return data.collect()