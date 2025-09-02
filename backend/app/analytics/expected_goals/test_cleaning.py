import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import pytest

import polars as pl
import polars.testing

from . import cleaning

@pytest.fixture
def notNullDefendingSideRight():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'timeInPeriodSec': [30],
        'typeCode': [506],
        'homeTeamDefendingSide': ['right'],
        'zoneCode': ['O'],
        'xCoord': [-30],
        'yCoord': [5],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def notNullDefendingSideLeft():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'timeInPeriodSec': [30],
        'typeCode': [506],
        'homeTeamDefendingSide': ['left'],
        'zoneCode': ['O'],
        'xCoord': [30],
        'yCoord': [2],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def nullDefendingSideRight():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'timeInPeriodSec': [30],
        'typeCode': [506],
        'homeTeamDefendingSide': [None],
        'zoneCode': ['O'],
        'xCoord': [-30],
        'yCoord': [5],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def nullDefendingSideLeft():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'timeInPeriodSec': [30],
        'typeCode': [506],
        'homeTeamDefendingSide': [None],
        'zoneCode': ['O'],
        'xCoord': [30],
        'yCoord': [2],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def nullMixedDefendingSide():
    return pl.DataFrame({
        'gameID': [1, 1, 1, 1, 2],
        'period': [1, 1, 1, 2, 1],
        'timeInPeriodSec': [20, 30, 32, 5, 3],
        'typeCode': [506, 506, 516, 506, 506],
        'homeTeamDefendingSide': [None, None, None, None, None],
        'zoneCode': ['O', 'O', 'N', 'O', 'O'],
        'xCoord': [-30, 30, 0, -30, -40],
        'yCoord': [0, 0, 0, 0, 0],
        'eventOwnerTeamID': [30, 20, 30, 20, 45],
        'homeTeamID': [20, 20, 20, 20, 45],
        'awayTeamID': [30, 30, 30, 30, 30]
    })

@pytest.fixture
def notNullMixedDefendingSide():
    return pl.DataFrame({
        'gameID': [1, 1, 1, 1, 2],
        'period': [1, 1, 1, 2, 1],
        'timeInPeriodSec': [20, 30, 32, 5, 3],
        'typeCode': [506, 506, 516, 506, 506],
        'homeTeamDefendingSide': ['left', 'left', 'left', 'right', 'right'],
        'zoneCode': ['O', 'O', 'N', 'O', 'O'],
        'xCoord': [-30, 30, 0, -30, -40],
        'yCoord': [0, 0, 0, 0, 0],
        'eventOwnerTeamID': [30, 20, 30, 20, 45],
        'homeTeamID': [20, 20, 20, 20, 45],
        'awayTeamID': [30, 30, 30, 30, 30]
    })

@pytest.fixture
def mixedPeriods():
    return pl.DataFrame({
        "id": [1, 2, 3, 4],
        "gameID": [320, 320, 320, 320],
        "typeCode": [502, 503, 504, 505],
        "eventOwnerTeamID": [30, 30, 30, 30],
        "period": [1, 1, 2, 2],
        "xCoord": [10.5, 20.1, 30.2, 40.3],
        "yCoord": [5.2, 15.3, 25.4, 35.5],
        "timeInPeriodSec": [100, 110, 120, 140]
    })

class TestAddLastEvent:

    def test_last_event_times(self, mixedPeriods):
        new_df = cleaning.add_last_event(mixedPeriods)
        polars.testing.assert_series_equal(pl.Series([None, 10, None, 20], dtype=pl.Int64), new_df.select("timeSinceLastEvent").to_series(), check_names=False)

    def test_last_event_coordinates(self, mixedPeriods):
        new_df = cleaning.add_last_event(mixedPeriods)
        target = pl.DataFrame({
            "lastEventXCoord": [None, 10.5, None, 30.2],
            "lastEventYCoord": [None, 5.2, None, 25.4]
        })
        polars.testing.assert_frame_equal(new_df.select("lastEventXCoord", "lastEventYCoord"), target)

    def test_last_event_typecodes(self, mixedPeriods):
        new_df = cleaning.add_last_event(mixedPeriods)
        polars.testing.assert_series_equal(pl.Series([None, 502, None, 504], dtype=pl.Int64), new_df.select("lastEventTypeCode").to_series(), check_names=False)

    def test_last_event_distance(self, mixedPeriods):
        new_df = cleaning.add_last_event(mixedPeriods)
        polars.testing.assert_series_equal(pl.Series([None, cleaning.get_distance_between(10.5, 5.2, 20.1, 15.3), None, cleaning.get_distance_between(30.2, 25.4, 40.3, 35.5)]),
                                           new_df.select("distFromLastEvent").to_series(), check_names=False)

class TestSetSide:

    def test_set_side_period_clean(self, notNullDefendingSideRight, notNullDefendingSideLeft):
        newDataRight = notNullDefendingSideRight.pipe(cleaning.set_side_period)
        newDataLeft = notNullDefendingSideLeft.pipe(cleaning.set_side_period)
        polars.testing.assert_frame_equal(notNullDefendingSideRight, newDataRight)
        polars.testing.assert_frame_equal(notNullDefendingSideLeft, newDataLeft)

    def test_set_side_period_right(self, nullDefendingSideRight, notNullDefendingSideRight):
        newData = nullDefendingSideRight.pipe(cleaning.set_side_period)
        polars.testing.assert_frame_equal(notNullDefendingSideRight, newData)

    def test_set_side_period_left(self, nullDefendingSideLeft, notNullDefendingSideLeft):
        newData = nullDefendingSideLeft.pipe(cleaning.set_side_period)
        polars.testing.assert_frame_equal(notNullDefendingSideLeft, newData)

    def test_set_side_period_mixed(self, nullMixedDefendingSide, notNullMixedDefendingSide):
        newData = nullMixedDefendingSide.pipe(cleaning.set_side, preserve_order=True)
        polars.testing.assert_frame_equal(notNullMixedDefendingSide, newData)

