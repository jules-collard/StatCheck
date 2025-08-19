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
    return pd.DataFrame([[1, 1, 505, 'right', -10, 1, 1, 2],
                         [1, 1, 505, 'right', -10, 2, 1, 2],
                         [1, 2, 505, 'left', 10, 1, 1, 2],
                         [1, 2, 505, 'left', -10, 2, 1, 2]],
                         columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'xCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID'])

class TestSetSide:

    def test_clean(self, singleLineDataset):
        newData = singleLineDataset.groupby(['gameID','period'])[singleLineDataset.columns].apply(expected_goals.set_side, include_groups=False)
        assert all(a == b for a,b in zip([1, 1, 505, 'right', 'O', -10], newData.iloc[0].to_list()))

    def test_dirty(self, nullSideDataset):
        newData = nullSideDataset.groupby(['gameID','period']).apply(expected_goals.set_side, include_groups=False).reset_index()
        assert newData['homeTeamDefendingSide'].iloc[0] == 'right'

class TestStdCoordinates:

    def test(self, multiLineDataset):
        standardisedData = multiLineDataset.groupby(['gameID', 'period']).apply(expected_goals.standardise_coordinates, include_groups=False)
        goal = [10, -10, 10, 10]
        assert [a == b for a,b in zip(standardisedData['xStd'].to_list(), goal)]