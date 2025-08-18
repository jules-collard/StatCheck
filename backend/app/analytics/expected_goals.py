from app import app, db

import pandas as pd
import sqlalchemy as sa

from app.updaters.games import Event, Game

def set_side(group: pd.DataFrame):
    if not group['homeTeamDefendingSide'].isnull().any():
        return group
    elif group[(group["zoneCode"] == 'O') & (group["eventOwnerTeamID"] == group["homeTeamID"])]["xCoord"].iloc[0] < 0:
        group.loc[:, 'homeTeamDefendingSide'] = 'right'
    else:
        group.loc[:, 'homeTeamDefendingSide'] = 'left'
    return group

def standardise_coordinates(group: pd.DataFrame):
    group.loc[:, 'xStd'] = None
    if group['homeTeamDefendingSide'].iloc[0] == 'right':
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
    else:
        group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xStd'] = group.loc[group['eventOwnerTeamID'] == group['homeTeamID'], 'xCoord']
        group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xStd'] = -group.loc[group['eventOwnerTeamID'] == group['awayTeamID'], 'xCoord']
    return group

def clean(group):
    group = set_side(group)
    group = standardise_coordinates(group)
    return group

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
    events['timeLastEvent'] = events.groupby(['gameID', 'period'])['timeInPeriodSec'].shift(1)
    fenwickEvents = events[events['typeCode'].isin([505,506,507])]
    fenwickEvents = fenwickEvents.groupby(['gameID', 'period']).apply(clean, include_groups = False)

    print(fenwickEvents.groupby(['gameID', 'period']).head(10)[['timeInPeriodSec', 'typeCode', 'homeTeamDefendingSide', 'eventOwnerTeamID', 'homeTeamID', 'awayTeamID', 'xCoord', 'xStd']])


# print(f"Missing x Coordinates: {fenwickEvents['xCoord'].isna().mean() * 100}%")
# print(f"Missing y Coordinates: {fenwickEvents['yCoord'].isna().mean() * 100}%")