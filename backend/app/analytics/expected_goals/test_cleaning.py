import pytest
import polars as pl
import polars.testing
import polars.selectors as cs

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

@pytest.fixture
def standardiseCoordinatesHomeFlip():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'homeTeamDefendingSide': ['right'],
        'xCoord': [-30],
        'yCoord': [-5],
        'lastEventXCoord': [-25],
        'lastEventYCoord': [-3],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def standardiseCoordinatesHomeKeep():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'homeTeamDefendingSide': ['left'],
        'xCoord': [30],
        'yCoord': [5],
        'lastEventXCoord': [25],
        'lastEventYCoord': [3],
        'eventOwnerTeamID': [20],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def standardiseCoordinatesAwayFlip():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'homeTeamDefendingSide': ['left'],
        'xCoord': [-30],
        'yCoord': [-5],
        'lastEventXCoord': [-25],
        'lastEventYCoord': [-3],
        'eventOwnerTeamID': [30],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def standardiseCoordinatesAwayKeep():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'homeTeamDefendingSide': ['right'],
        'xCoord': [30],
        'yCoord': [5],
        'lastEventXCoord': [25],
        'lastEventYCoord': [3],
        'eventOwnerTeamID': [30],
        'homeTeamID': [20],
        'awayTeamID': [30]
    })

@pytest.fixture
def targetStdCoordinates():
    return pl.DataFrame({
        'xStd': [30],
        'yStd': [5],
        'lastEventXStd': [25],
        'lastEventYStd': [3]
    })

@pytest.fixture
def powerplay():
    return pl.DataFrame({
        'gameID': [2],
        'period': [2],
        'homeSkaters': [5],
        'awaySkaters': [4],
        'homeGoalie': [1],
        'awayGoalie': [1],
        'homeTeamID': [10],
        'awayTeamID': [20],
        'eventOwnerTeamID': [10]
    })

@pytest.fixture
def shorthanded():
    return pl.DataFrame({
        'gameID': [3],
        'period': [3],
        'homeSkaters': [5],
        'awaySkaters': [4],
        'homeGoalie': [1],
        'awayGoalie': [1],
        'homeTeamID': [10],
        'awayTeamID': [20],
        'eventOwnerTeamID': [20]
    })
    
@pytest.fixture
def evenStrength():
    return pl.DataFrame({
        'gameID': [1],
        'period': [1],
        'homeSkaters': [5],
        'awaySkaters': [5],
        'homeGoalie': [1],
        'awayGoalie': [1],
        'homeTeamID': [10],
        'awayTeamID': [20],
        'eventOwnerTeamID': [10]
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
        
class TestStdCoordinates:

    def test_home_coord_flip(self, standardiseCoordinatesHomeFlip, targetStdCoordinates):
        newData = standardiseCoordinatesHomeFlip.pipe(cleaning.standardise_coordinates)
        polars.testing.assert_frame_equal(newData.select(cs.ends_with('Std')), targetStdCoordinates)

    def test_home_coord_keep(self, standardiseCoordinatesHomeKeep, targetStdCoordinates):
        newData = standardiseCoordinatesHomeKeep.pipe(cleaning.standardise_coordinates)
        polars.testing.assert_frame_equal(newData.select(cs.ends_with('Std')), targetStdCoordinates)

    def test_away_coord_flip(self, standardiseCoordinatesAwayFlip, targetStdCoordinates):
        newData = standardiseCoordinatesAwayFlip.pipe(cleaning.standardise_coordinates)
        polars.testing.assert_frame_equal(newData.select(cs.ends_with('Std')), targetStdCoordinates)

    def test_away_coord_keep(self, standardiseCoordinatesAwayKeep, targetStdCoordinates):
        newData = standardiseCoordinatesAwayKeep.pipe(cleaning.standardise_coordinates)
        polars.testing.assert_frame_equal(newData.select(cs.ends_with('Std')), targetStdCoordinates)

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

class TestAddStrengths:

    def test_even_strength(self, evenStrength):
        newData = evenStrength.pipe(cleaning.add_strengths)
        result = newData.row(0, named=True)
        assert result['manAdvantage'] == 0

    def test_powerplay(self, powerplay):
        newData = powerplay.pipe(cleaning.add_strengths)
        result = newData.row(0, named=True)
        assert result['manAdvantage'] == 1

    def test_shorthanded(self, shorthanded):
        newData = shorthanded.pipe(cleaning.add_strengths)
        result = newData.row(0, named=True)
        assert result['manAdvantage'] == -1

class TestGeometry:

    def test_get_shot_angle(self):
        # Typical case
        assert cleaning.get_shot_angle(88.5, 0) == 0
        # Positive y
        angle = cleaning.get_shot_angle(80, 10)
        assert isinstance(angle, float)
        # None input
        assert cleaning.get_shot_angle(None, 10) is None
        assert cleaning.get_shot_angle(80, None) is None


    def test_get_shot_distance(self):
        # Typical case
        dist = cleaning.get_shot_distance(88.5, 0)
        assert isinstance(dist, float)
        # Check known value
        assert cleaning.get_shot_distance(89, 0) == 0


    def test_get_distance_between(self):
        # Typical case
        dist = cleaning.get_distance_between(0, 0, 3, 4)
        assert dist == 5
        # None input
        assert cleaning.get_distance_between(None, 0, 3, 4) is None
        assert cleaning.get_distance_between(0, None, 3, 4) is None
        assert cleaning.get_distance_between(0, 0, None, 4) is None
        assert cleaning.get_distance_between(0, 0, 3, None) is None


    def test_get_angle_change_speed(self):
        # Typical case
        speed = cleaning.get_angle_change_speed(10, 20, 2)
        assert speed == 5
        # Zero time
        assert cleaning.get_angle_change_speed(10, 20, 0) is None
        # None input
        assert cleaning.get_angle_change_speed(None, 20, 2) is None
        assert cleaning.get_angle_change_speed(10, None, 2) is None
        assert cleaning.get_angle_change_speed(10, 20, None) is None

