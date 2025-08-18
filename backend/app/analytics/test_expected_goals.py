import pandas as pd
from app.analytics import expected_goals

class TestSetSide:

    def test_clean(self):
        cleanData = pd.DataFrame([[1, 1, 505, 'right', 'O', -10]],
            columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord'],
        )
        newCleanData = cleanData.groupby(['gameID','period'])[cleanData.columns].apply(expected_goals.set_side, include_groups=False)
        assert all(a == b for a,b in zip([1, 1, 505, 'right', 'O', -10], newCleanData.iloc[0].to_list()))

    def test_dirty(self):
        dirtyData = pd.DataFrame([[1, 1, 505, None, 'O', -10, 1, 1]],
            columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'zoneCode', 'xCoord', 'eventOwnerTeamID', 'homeTeamID']
        )
        newDirtyData = dirtyData.groupby(['gameID','period']).apply(expected_goals.set_side, include_groups=False).reset_index()
        assert newDirtyData['homeTeamDefendingSide'].iloc[0] == 'right'

class TestStdCoordinates:

    def test(self):
        data = pd.DataFrame([[1, 1, 505, 'right', -10, 1, 1, 2],
                             [1, 1, 505, 'right', -10, 2, 1, 2],
                             [1, 2, 505, 'left', 10, 1, 1, 2],
                             [1, 2, 505, 'left', -10, 2, 1, 2]],
            columns=['gameID', 'period', 'typeCode', 'homeTeamDefendingSide', 'xCoord', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID'],
        )
        standardisedData = data.groupby(['gameID', 'period']).apply(expected_goals.standardise_coordinates, include_groups=False)
        standardised = [10, -10, 10, 10]

        assert [a == b for a,b in zip(standardisedData['xStd'].to_list(), standardised)]