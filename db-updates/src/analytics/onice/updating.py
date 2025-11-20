from typing import List

import requests
import polars as pl
from polars import col as c

from src import BACKEND_URL
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
        event_data
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
    return q

def get_split_shifts(gameID: int):
    all_events = []
    shifts = get_shifts(gameID)
    for shift in shifts:
        events = get_shift_events(shift)
        shift_events = clean_shift_events(shift, events)
        all_events.append(shift_events)

    all_events_df: pl.DataFrame = pl.concat(all_events)
    all_events_df = (all_events_df
                     .pipe(add_strengths)
                     .pipe(add_faceoff_zone)
                     .pipe(add_score))
    splitshifts = calculate_shift_data(all_events_df)
    return [SplitShiftBase(**splitshift) for splitshift in splitshifts.to_dicts()]

def post_split_shifts(gameID: int, splitshifts: List[SplitShiftBase]):
    r = requests.post(f"{BACKEND_URL}/games/{gameID}/split-shifts", json=splitshifts)
    print(f"{gameID} Split-Shifts: {r.status_code}")
