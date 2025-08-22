import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import pytest

from app.analytics import expected_goals

@pytest.fixture
def notNullDefendingSideRight():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, 'right', 'O', -30, 5, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def notNullDefendingSideRightStd():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, 'right', 'O', -30, 5, 30, -5, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'xStd', 'yStd', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def notNullDefendingSideLeft():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, 'left', 'O', 30, 2, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def notNullDefendingSideLeftStd():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, 'left', 'O', 30, 2, 30, 2, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'xStd', 'yStd', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def nullDefendingSideRight():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, np.nan, 'O', -30, 5, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def nullDefendingSideLeft():
    return pd.DataFrame(
        [
            [1, 1, 30, 506, np.nan, 'O', 30, 2, 20, 20, 30]
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def nullMixedDefendingSide():
    return pd.DataFrame(
        [
            [1, 1, 20, 506, np.nan, 'O', -30, 0, 30, 20, 30], # Left
            [1, 1, 30, 506, np.nan, 'O', 30, 0, 20, 20, 30], # Left
            [1, 1, 32, 516, np.nan, 'N', 0, 0, 30, 20, 30], # Left
            [1, 2, 5, 506, np.nan, 'O', -30, 0, 20, 20, 30], # Right
            [2, 1, 3, 506, np.nan, 'O', -40, 0, 45, 45, 30] # right
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )

@pytest.fixture
def notNullMixedDefendingSide():
    return pd.DataFrame(
        [
            [1, 1, 20, 506, 'left', 'O', -30, 0, 30, 20, 30], # Left
            [1, 1, 30, 506, 'left', 'O', 30, 0, 20, 20, 30], # Left
            [1, 1, 32, 516, 'left', 'N', 0, 0, 30, 20, 30], # Left
            [1, 2, 5, 506, 'right', 'O', -30, 0, 20, 20, 30], # Right
            [2, 1, 3, 506, 'right', 'O', -40, 0, 45, 45, 30] # right
        ],
        columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID']
    )


class TestSetSide:
    
    def test_set_side_period_clean(self, notNullDefendingSideRight):
        newData = notNullDefendingSideRight.pipe(expected_goals.set_side_period)
        assert_frame_equal(newData, notNullDefendingSideRight)

    def test_set_side_period_right(self, nullDefendingSideRight, notNullDefendingSideRight):
        newData = nullDefendingSideRight.pipe(expected_goals.set_side_period)
        assert_frame_equal(newData, notNullDefendingSideRight)

    def test_set_side_period_left(self, nullDefendingSideLeft, notNullDefendingSideLeft):
        newData = nullDefendingSideLeft.pipe(expected_goals.set_side_period)
        assert_frame_equal(newData, notNullDefendingSideLeft)

    def test_set_defending_side(self, nullMixedDefendingSide, notNullMixedDefendingSide):
        newData = nullMixedDefendingSide.pipe(expected_goals.set_defending_side)
        assert_frame_equal(newData, notNullMixedDefendingSide)

class TestCoordinates:
    
    def test_standardise_coordinates_period_right(self, notNullDefendingSideRight, notNullDefendingSideRightStd):
        right = notNullDefendingSideRight.copy()
        right['lastEventXCoord'] = right['xCoord']
        right['lastEventYCoord'] = right['yCoord']

        rightStd = notNullDefendingSideRightStd.copy()
        rightStd['lastEventXCoord'] = rightStd['xCoord']
        rightStd['lastEventYCoord'] = rightStd['yCoord']
        rightStd['lastEventXStd'] = rightStd['xStd']
        rightStd['lastEventYStd'] = rightStd['yStd']
        
        newData = right.pipe(expected_goals.standardise_coordinates_period)
        assert_frame_equal(newData, rightStd, check_like=True, check_dtype=False)

    def test_standardise_coordinates_period_left(self, notNullDefendingSideLeft, notNullDefendingSideLeftStd):
        left = notNullDefendingSideLeft.copy()
        left['eventOwnerTeamID'] = left['awayTeamID']
        left['lastEventXCoord'] = left['xCoord']
        left['lastEventYCoord'] = left['yCoord']
        
        leftStd = notNullDefendingSideLeftStd.copy()
        leftStd['eventOwnerTeamID'] = leftStd['awayTeamID']
        leftStd['lastEventXCoord'] = leftStd['xCoord']
        leftStd['lastEventYCoord'] = leftStd['yCoord']
        leftStd['xStd'] = -leftStd['xStd']
        leftStd['yStd'] = -leftStd['yStd']
        leftStd['lastEventXStd'] = leftStd['xStd']
        leftStd['lastEventYStd'] = leftStd['yStd']

        newData = left.pipe(expected_goals.standardise_coordinates_period)
        assert_frame_equal(newData, leftStd, check_like=True, check_dtype=False)


class TestGeometry:
    def test_shot_angle_on_goal(self):
        assert expected_goals.get_shot_angle(88, 0) == 0

    def test_shot_angle_positive_1(self):
        assert expected_goals.get_shot_angle(78, 10) > 0

    def test_shot_angle_positive_2(self):
        assert expected_goals.get_shot_angle(98, -10) > 0

    def test_shot_angle_goal_line(self):
        assert expected_goals.get_shot_angle(88, 20) == 90

    def test_shot_angle_nan(self):
        assert np.isnan(expected_goals.get_shot_angle(np.nan, 10))

    def test_shot_distance_center(self):
        assert expected_goals.get_shot_distance(88, 0) == 0.0

    def test_shot_distance_typical(self):
        result = expected_goals.get_shot_distance(78, 10)
        expected = np.sqrt(10**2 + (88-78)**2)
        assert np.isclose(result, expected)

    def test_shot_distance_vertical(self):
        assert expected_goals.get_shot_distance(88, 20) == 20.0

    def test_shot_distance_nan_both(self):
        result = expected_goals.get_shot_distance(np.nan, np.nan)
        assert np.isnan(result)

    def test_distance_between_nan(self):
        assert np.isnan(expected_goals.get_distance_between(np.nan, 0, 0, 0))