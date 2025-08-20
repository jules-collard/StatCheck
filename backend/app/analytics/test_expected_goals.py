import pandas as pd
import pytest

from app.analytics import expected_goals

@pytest.fixture
def singleLineDataset():
    return  pd.DataFrame([[1, 1, 505, 'right', 'O', -10, 1, 1]],
                         columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'eventOwnerTeamID', 'homeTeamID'])

@pytest.fixture
def nullSideDataset():
    return  pd.DataFrame([[1, 1, 505, None, 'O', -10, 1, 1]],
                         columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'eventOwnerTeamID', 'homeTeamID'])

@pytest.fixture
def multiLineDataset():
    return pd.DataFrame([[1, 1, 0, 505, 'right', -10, 0, 1, 1, 2],
                         [1, 1, 2, 506, 'right', -10, 0, 2, 1, 2],
                         [1, 2, 5, 506, 'left', 10, 0, 1, 1, 2],
                         [1, 2, 10, 505, 'left', -10, 0, 2, 1, 2]],
                         columns=['gameID', 'period', 'timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'xCoord', 'yCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID'])

class TestCleaning:

    def test_set_defending_side_clean(self, singleLineDataset):
        newData = singleLineDataset.pipe(expected_goals.set_defending_side)
        assert all(a == b for a,b in zip([1, 1, 505, 'right', 'O', -10], newData.iloc[0].to_list()))

    def test_set_defending_side_dirty(self, nullSideDataset):
        newData = nullSideDataset.pipe(expected_goals.set_defending_side)
        assert newData['homeTeamDefendingSide'].iloc[0] == 'right'

    def test_std_coordinates(self, multiLineDataset):
        standardisedData = multiLineDataset.pipe(expected_goals.standardise_coordinates).xStd
        goal = [10, -10, 10, 10]
        assert all([a == b for a,b in zip(standardisedData.to_list(), goal)])

    def test_add_last_event(self, multiLineDataset):
        newData = multiLineDataset.pipe(expected_goals.add_last_event)
        assert (all([a == b for a,b in zip([0, 5], newData['timeLastEvent'].dropna().to_list())])
                and all([a == b for a,b in zip([2, 5], newData['timeDiff'].dropna().to_list())]))
        
    def test_add_shot_information(self, multiLineDataset):
        newData = (multiLineDataset
                   .pipe(expected_goals.add_last_event)
                   .pipe(expected_goals.standardise_coordinates)
                   .pipe(expected_goals.add_shot_information))
        assert (
            all([a == b] for a,b in zip([1,0,0,1], newData.isGoal.to_list())) and
            all([a == b] for a,b in zip([1,0], newData.isRebound.dropna().to_list())) and
            all([a == b] for a,b in zip([0,0,0,0], newData.shotAngle.to_list())) and
            all([a == b] for a,b in zip([abs(88-x) for x in newData.xStd.to_list()], newData.shotDistance.to_list()))
        )

