from sklearn.impute import SimpleImputer
from app import app, db
from app.models import Event, Game

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

TYPECODES = {
    502: 'faceoff',
    502: 'hit',
    504: 'giveaway',
    505: 'goal',
    506: 'shot-on-goal',
    507: 'missed-shot',
    508: 'blocked-shot',
    525: 'takeaway',
    537: 'failed-shot-attempt'
}

SHOTTYPES = ['backhand', 'deflected', 'slap', 'snap', 'tip-in', 'wrap-around', 'wrist']

def set_side_period(group: pd.DataFrame):
    group = group.copy()
    if not group['homeTeamDefendingSide'].isnull().any():
        return group
    elif len(group.query('zoneCode == "O" & eventOwnerTeamID == homeTeamID')) > 0:
        if group.query('zoneCode == "O" & eventOwnerTeamID == homeTeamID').xCoord.iloc[0] < 0:
            group['homeTeamDefendingSide'] = 'right'
        else:
            group['homeTeamDefendingSide'] = 'left'
    elif len(group.query('zoneCode == "O" & eventOwnerTeamID == awayTeamID')) > 0:
        if group.query('zoneCode == "O" & eventOwnerTeamID == awayTeamID').xCoord.iloc[0] < 0:
            group['homeTeamDefendingSide'] = 'left'
        else:
            group['homeTeamDefendingSide'] = 'right'
    else:
        group['homeTeamDefendingSide'] = None
    
    return group

def set_defending_side(data: pd.DataFrame):
    data = data.copy()
    data['homeTeamDefendingSide'] = (data
                                     .groupby(['gameID', 'period'])
                                     .apply(set_side_period, include_groups = False)
                                     .homeTeamDefendingSide
                                     .to_list())
    return data

def standardise_coordinates_period(group: pd.DataFrame):
    group = group.copy()
    group['xStd'] = None
    group['yStd'] = None
    group['lastEventXStd'] = None
    group['lastEventYStd'] = None
    if group['homeTeamDefendingSide'].iloc[0] == 'right':
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'yStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'yCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'yStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'yCoord']

        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventXStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventXCoord']
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventYStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventYCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventXStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventXCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventYStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventYCoord']
    else:
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'yStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'yCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'yStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'yCoord']

        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventXStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventXCoord']
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventYStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'lastEventYCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventXStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventXCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventYStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'lastEventYCoord']
    return group

def standardise_coordinates(data: pd.DataFrame):
    data = data.copy()
    newCoords = (data
                    .groupby(['gameID', 'period'])
                    .apply(standardise_coordinates_period, include_groups = False))[['xStd', 'yStd', 'lastEventXStd', 'lastEventYStd']].to_numpy().T
    data['xStd'] = newCoords[0]
    data['yStd'] = newCoords[1]
    data['lastEventXStd'] = newCoords[2]
    data['lastEventYStd'] = newCoords[3]
    return data

def add_last_event(data: pd.DataFrame):
    data = data.copy()
    lastEvent = (data
                    .groupby(['gameID', 'period'])
                    .shift(1))[['timeInPeriodSec', 'typeCode', 'xCoord', 'yCoord']].to_numpy().T
    data['timeSinceLastEvent'] = data['timeInPeriodSec'] - lastEvent[0]
    data['lastEventTypeCode'] = lastEvent[1]
    data['lastEventTypeCode'] = (data['lastEventTypeCode']).astype('Int64')
    data['lastEventXCoord'] = lastEvent[2]
    data['lastEventYCoord'] = lastEvent[3]
    data['distFromLastEvent'] = data.apply(lambda row: get_distance_between(row['lastEventXCoord'], row['lastEventYCoord'], row['xCoord'], row['yCoord']), axis = 1)
    data['speedFromLastEvent'] = data.apply(lambda row: get_speed(row['lastEventXCoord'], row['lastEventYCoord'], row['xCoord'], row['yCoord'], row['timeSinceLastEvent']), axis = 1)

    return data

def add_shot_information(data: pd.DataFrame):
    data = data.copy()
    data['isGoal'] = (data['typeCode'] == 505).astype(int)
    data['shotAngle'] = data.apply(lambda row: get_shot_angle(row['xStd'], row['yCoord']), axis = 1)
    data['shotDistance'] = data.apply(lambda row: get_shot_distance(row['xStd'], row['yCoord']), axis = 1)
    return data

def add_angle_change_speed(data: pd.DataFrame):
    data = data.copy()
    data['lastShotAngle'] = np.nan
    data['angleChangeSpeed'] = np.nan
    data.loc[(data['lastEventTypeCode'] == 506) & (data['timeSinceLastEvent'] < 3), 'lastShotAngle'] = (data.loc[(data['lastEventTypeCode'] == 506) & (data['timeSinceLastEvent'] < 3), ['lastEventXStd', 'lastEventYStd']]
                                                                                                        .apply(lambda row: get_shot_angle(row['lastEventXStd'], row['lastEventYStd']), axis = 1))
    data.loc[(data['lastEventTypeCode'] == 506) & (data['timeSinceLastEvent'] < 3), 'angleChangeSpeed'] = (data.loc[(data['lastEventTypeCode'] == 506) & (data['timeSinceLastEvent'] < 3), ['shotAngle', 'lastShotAngle', 'timeSinceLastEvent']]
                                                                                                            .apply(lambda row: get_angle_change_speed(row['lastShotAngle'], row['shotAngle'], row['timeSinceLastEvent']), axis = 1))
    return data

def add_strengths(data: pd.DataFrame):
    data = data.copy()
    data['attackingSkaters'] = data.apply(lambda row: (row.homeSkaters if row.eventOwnerTeamID == row.homeTeamID else row.awaySkaters), axis=1)
    data['defendingSkaters'] = data.apply(lambda row: (row.awaySkaters if row.eventOwnerTeamID == row.homeTeamID else row.homeSkaters), axis=1)
    data['manAdvantage'] = data['attackingSkaters'] - data['defendingSkaters']
    data['goalieInNet'] = data.apply(lambda row: (row.awayGoalie if row.eventOwnerTeamID == row.homeTeamID else row.homeGoalie), axis=1)
    return data

def get_shot_angle(x: float, y: float):
    if np.isnan(x) or np.isnan(y):
        return np.nan
    ratio = y / np.sqrt(y**2 + (88 - x)**2)
    angle = abs(np.asin(ratio)) * 180 / np.pi
    return 0 if np.isnan(angle) else angle

def get_shot_distance(x: float, y: float):
    return np.sqrt(y**2 + (88-x)**2)

def get_distance_between(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_speed(x1, y1, x2, y2, time):
    if any([np.isnan(num) for num in [x1, y1, x2, y2, time]]) or time == 0:
        return np.nan
    
    dist = get_distance_between(x1, y1, x2, y2)
    return dist / time

def get_angle_change_speed(angle1, angle2, time):
    if time == 0:
        return np.nan
    else:
        return abs(angle2 - angle1) / time

def extract_covariate_columns(data: pd.DataFrame):
    return data.copy()[['shotDistance', 'timeSinceLastEvent', 'shotType', 'speedFromLastEvent', 'shotAngle', 'angleChangeSpeed', 'lastEventTypeCode', 'manAdvantage', 'defendingSkaters', 'goalieInNet', 'distFromLastEvent', 'xStd', 'yStd']]

def extract_target_column(data: pd.DataFrame):
    return data.copy().isGoal

def typecode_descriptions(data: pd.DataFrame):
    data = data.copy()
    data['lastEventTypeCode'] = data['lastEventTypeCode'].map(TYPECODES)
    print()
    return data

def get_clean_data(start_season: int, end_season: int):
    app.app_context().push()
    data = (db.session.query(Event.gameID, Event.id, Event.timeInPeriodSec, Event.sortOrder, Event.typeCode, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.homeTeamDefendingSide, Event.period, Event.eventOwnerTeamID, Event.shootingPlayerID, Event.xCoord, Event.yCoord, Event.zoneCode, Event.shotType, Game.homeTeamID, Game.awayTeamID)
            .filter(Game.season >= start_season, Game.season <= end_season)
            .filter(Game.gameType == 2)
            .filter(Event.periodType != 'SO')
            .filter(Event.typeCode.in_(TYPECODES.keys()))
            .join(Event.game)
            .order_by(Game.id, Event.period, Event.timeInPeriodSec ,Event.sortOrder)
            .all())
    
    data = pd.DataFrame(data)
    data = (data
            .pipe(add_last_event)
            .query('typeCode.isin([505,506,507])')
            .pipe(set_defending_side)
            .dropna(subset=['xCoord', 'yCoord'])
            .pipe(standardise_coordinates)
            .pipe(add_shot_information)
            .pipe(add_angle_change_speed)
            .pipe(add_strengths)
            .query('defendingSkaters > 0') # Remove penalty shots
            .pipe(typecode_descriptions)
            .reset_index())
    
    features = data.pipe(extract_covariate_columns)
    target = data.pipe(extract_target_column)

    typecode_categories = [*TYPECODES.values(), 'missing']
    shottype_categories = [*SHOTTYPES, 'missing']

    categorical_transformer = Pipeline(steps=[
        ('nan-imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('none-imputer', SimpleImputer(strategy='constant', missing_values=None, fill_value='missing')),
        ('onehot', OneHotEncoder(categories=[typecode_categories, shottype_categories]))
    ])

    categorical_features = ['lastEventTypeCode', 'shotType']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough',
        verbose_feature_names_out=False
    )

    transformed_features = preprocessor.fit_transform(features).astype(float)
    feature_names = preprocessor.get_feature_names_out()
    transformed_df = pd.DataFrame(transformed_features, columns=feature_names).astype(float)

    return transformed_df, target

if __name__ == "__main__":
    x, y = get_clean_data(20142015, 20142015)
    print(x.columns)