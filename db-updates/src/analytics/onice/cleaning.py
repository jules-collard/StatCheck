import polars as pl
import polars.selectors as cs
from polars import col as c

from src.models.shifts import ShiftBase

schema = {
    'period': pl.Int8,
    'timeInPeriodSec': pl.Int16,
    'awayGoalie': pl.Int8,
    'awaySkaters': pl.Int8,
    'homeGoalie': pl.Int8,
    'homeSkaters': pl.Int8,
    'typeCode': pl.Int16,
    'xStd': pl.Float32,
    'homeScore': pl.Int8,
    'awayScore': pl.Int8,
    'eventOwnerTeamID': pl.Int8,
    'homeTeamID': pl.Int8,
    'xg': pl.Float64
}

def get_shift_start_event(period: int, startTime: int, awayGoalie, awaySkaters, homeGoalie, homeSkaters, awayScore, homeScore):
    return {
        'period': period,
        'timeInPeriodSec': startTime,
        'awayGoalie': awayGoalie,
        'awaySkaters': awaySkaters,
        'homeGoalie': homeGoalie,
        'homeSkaters': homeSkaters,
        'awayScore': awayScore,
        'homeScore': homeScore,
        'typeCode': 600,
        'xStd': None,
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
        'homeScore': None,
        'awayScore': None,
        'typeCode': 601,
        'xStd': None,
        'eventOwnerTeamID': None,
        'homeTeamID': None,
        'xg': None,
    }

def add_faceoff_zone(data: pl.DataFrame):
    q = data.with_columns(
        faceoffZone = pl.when(c('xStd') < -25)
                    .then(pl.lit('D'))
                    .when(c('xStd') > 25)
                    .then(pl.lit('O'))
                    .otherwise(pl.lit('N'))
                    .cast(pl.Enum(['D', 'N', 'O']))
    )
    return q

def add_strengths(data: pl.DataFrame):
    return (data
            .with_columns(attackingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('homeSkaters')).otherwise(c('awaySkaters')),
                          defendingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('awaySkaters')).otherwise(c('homeSkaters')),
                          attackingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('homeGoalie')).otherwise(c('awayGoalie')),
                          defendingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('awayGoalie')).otherwise(c('homeGoalie')))
            .with_columns(strengthState = pl.struct(['attackingSkaters', 'defendingSkaters', 'attackingGoalie', 'defendingGoalie']))
            .with_columns(split = c('strengthState').rle_id().over('shiftID')))

def add_score(data: pl.DataFrame):
    return (data
            .with_columns(
                scoreState = pl.when(c('homeTeamID') == c('teamID')).then(c('homeScore') - c('awayScore')).otherwise(c('awayScore') - c('homeScore'))
            ))

def clean_shift_events(shift: ShiftBase, events: list[dict]):
    if len(events) == 0:
        events_df = pl.Schema(schema).to_frame()
    else:
        events_df = (pl.from_dicts(data=events, schema=schema)
                .filter(((c('typeCode') == 502) & (c('timeInPeriodSec') == shift.endTimeSec)).not_(), # remove faceoff at end of shift
                        ((c('typeCode') == 516) & (c('timeInPeriodSec') == shift.startTimeSec)).not_())
                .drop_nulls(subset=['awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters'])) # Remove stoppage at start of shift
    
    if events_df.is_empty():
        first_strength_state = (1,5,1,5)
        last_strength_state = (1,5,1,5)
        first_score = (0,0)
    else:
        first_strength_state = events_df.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(0)
        last_strength_state = events_df.select('awayGoalie', 'awaySkaters', 'homeGoalie', 'homeSkaters').row(-1)
        first_score = events_df.select('awayScore', 'homeScore').row(0)
    
    start_event = get_shift_start_event(shift.period, shift.startTimeSec, *first_strength_state, *first_score)
    end_event = get_shift_end_event(shift.period, shift.endTimeSec, *last_strength_state)

    data = pl.concat([pl.DataFrame(start_event, schema=schema), events_df, pl.DataFrame(end_event, schema=schema)])
    
    data = (data
            .with_columns(teamID = shift.teamID,
                          playerID = shift.playerID,
                          gameID = shift.gameID,
                          shiftID = shift.id,
                          forPlayer = c('eventOwnerTeamID') == shift.teamID,
                          timeNextEvent = c('timeInPeriodSec').shift(-1)))
    return data