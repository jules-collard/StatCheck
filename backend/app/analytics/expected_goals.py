from app import app, db

import pandas as pd
import numpy as np
from app.models import Event, Game
import matplotlib.pyplot as plt

def set_side_period(group: pd.DataFrame):
    group = group.copy()
    if not group['homeTeamDefendingSide'].isnull().any():
        return group
    elif group.query('zoneCode == "O" & eventOwnerTeamID == homeTeamID').xCoord.iloc[0] < 0:
        group['homeTeamDefendingSide'] = 'right'
    else:
        group['homeTeamDefendingSide'] = 'left'
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
    if group['homeTeamDefendingSide'].iloc[0] == 'right':
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
    else:
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
    return group

def standardise_coordinates(data: pd.DataFrame):
    data = data.copy()
    data['xStd'] = (data
                    .groupby(['gameID', 'period'])
                    .apply(standardise_coordinates_period, include_groups = False)
                    .xStd
                    .to_list())
    return data

def add_last_event(data: pd.DataFrame):
    data = data.copy()
    data['timeLastEvent'] = (data
                             .groupby(['gameID', 'period'])
                             .timeInPeriodSec
                             .shift(1)
                             .to_list())
    data['timeDiff'] = data['timeInPeriodSec'] - data['timeLastEvent']
    return data

def add_shot_information(data: pd.DataFrame):
    data = data.copy()
    data['isGoal'] = (data['typeCode'] == 505).astype(int)
    data['isRebound']= (data['timeDiff'] < 3).astype(int)
    data['shotAngle'] = data.apply(lambda row: get_shot_angle(row['xStd'], row['yCoord']), axis = 1)
    data['shotDistance'] = data.apply(lambda row: get_shot_distance(row['xStd'], row['yCoord']), axis = 1)
    return data

def add_strengths(data: pd.DataFrame):
    data = data.copy()
    data['attackingSkaters'] = data.apply(lambda row: (row.homeSkaters if row.eventOwnerTeamID == row.homeTeamID else row.awaySkaters), axis=1)
    data['defendingSkaters'] = data.apply(lambda row: (row.awaySkaters if row.eventOwnerTeamID == row.homeTeamID else row.homeSkaters), axis=1)
    data['goalieInNet'] = data.apply(lambda row: (row.awayGoalie if row.eventOwnerTeamID == row.homeTeamID else row.homeGoalie), axis=1)
    return data

def get_shot_angle(x: float, y: float):
    ratio = y / np.sqrt(y**2 + (88 - x)**2)
    return abs(np.asin(ratio)) * 180 / np.pi

def get_shot_distance(x: float, y: float):
    return np.sqrt(y**2 + (88-x)**2)

if __name__ == "__main__":
    app.app_context().push()
    results = (db.session.query(Event.gameID, Event.id, Event.timeInPeriodSec, Event.sortOrder, Event.typeCode, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.homeTeamDefendingSide, Event.period, Event.eventOwnerTeamID, Event.shootingPlayerID, Event.xCoord, Event.yCoord, Event.zoneCode, Event.shotType, Game.homeTeamID, Game.awayTeamID)
            .filter(Event.gameID == 2021020061)
            .filter(Event.periodType != 'SO')
            .filter(Game.gameType == 2)
            .join(Event.game)
            .order_by(Game.id, Event.sortOrder)
            .all())
    
    events = pd.DataFrame(results)
    events = (events
              .pipe(add_last_event)
              .query('typeCode.isin([505,506,506])')
              .pipe(set_defending_side)
              .pipe(standardise_coordinates)
              .pipe(add_shot_information)
              .pipe(add_strengths))
    
    print(events.head(10))
