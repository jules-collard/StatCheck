from typing import List

import requests
import logfire
import polars as pl
from polars import col as c

from src.main import BACKEND_URL
from src.models.shifts import ShiftBase, SplitShiftBase
from .cleaning import clean_shift_events, add_faceoff_zone, add_score, add_strengths

def get_shifts(gameID: int):
    response = requests.get(f"{BACKEND_URL}/games/{gameID}/shifts").json()
    return [ShiftBase(**shift) for shift in response]

def get_shift_events(shift: ShiftBase):
    response = requests.get(f"{BACKEND_URL}/events/",
                            params={'gameID':shift.gameID,
                                    'period': shift.period,
                                    'startTimeSec': shift.startTimeSec,
                                    'endTimeSec': shift.endTimeSec}).json()
    return response

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
            c('scoreState').first().alias('score'),
            c('timeInPeriodSec').first().alias('startTimeSec'),
            c('timeNextEvent').last().fill_null(c('timeInPeriodSec').last()).alias('endTimeSec')
        )
        .with_columns(duration = c('endTimeSec') - c('startTimeSec'))
        .unnest('strengthState')
        .filter(c('duration') > 0)
    )
    return q.collect()

def get_split_shifts(shifts: List[ShiftBase]):
    if len(shifts) == 0:
        return []
    all_events = []
    for shift in shifts:
        events = get_shift_events(shift)
        shift_events = clean_shift_events(shift, events)
        all_events.append(shift_events)

    all_events_df: pl.DataFrame = pl.concat(all_events)
    all_events_df = (all_events_df
                     .pipe(add_strengths)
                     .pipe(add_faceoff_zone)
                     .pipe(add_score))
    splitshifts: pl.Dataframe = calculate_shift_data(all_events_df)
    return [SplitShiftBase(**splitshift) for splitshift in splitshifts.to_dicts()]

def post_split_shifts(gameID: int, splitshifts: List[SplitShiftBase]):
    if len(splitshifts) > 0:
        r = requests.post(f"{BACKEND_URL}/games/{gameID}/split-shifts", json=[spl.model_dump() for spl in splitshifts])
        logfire.info(f"{gameID} Split-Shifts: {r.status_code}", table='split_shifts', response_code=r.status_code)
    else:
        logfire.warn(f"No Split-Shifts for Game {gameID}", table='split_shifts')
