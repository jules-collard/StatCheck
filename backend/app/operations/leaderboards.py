import os
import json

from sqlalchemy import text
from pydantic import ValidationError

from app import app, db, ROOT_PATH
from app.models import Team
from app.api.api_models import SkaterLeaderboardItem, GoalieLeaderboardItem

def skater_row_to_object(row: dict):
    obj_dict = {key: row.get(key) for key in ['playerID', 'fullName', 'position', 'isActive', 'qualified']}
    totals = {key: row.get(key) for key in [
        'gamesPlayed', 'goals', 'assists', 'plusMinus', 'hits', 'sog', 'blocks', 'penaltyMinutes', 'avgTOI'
    ]}
    teamTriCodes = [db.session.get(Team, int(teamID)).triCode for teamID in row.get('teams').split(',')]

    obj_dict['totals'] = totals
    obj_dict['teamTriCodes'] = teamTriCodes
    obj = SkaterLeaderboardItem(**obj_dict)
    return obj.model_dump()

def goalie_row_to_object(row: dict):
    obj_dict = {key: row.get(key) for key in ['playerID', 'fullName', 'qualified', 'isActive']}
    totals = {key: row.get(key) for key in [
        'gamesPlayed', 'gamesStarted', 'wins', 'losses', 'goalsAgainst', 'goalsAgainstAvg', 'savePct', 'evenStrengthSavePct', 'powerPlaySavePct'
    ]}
    advanced = {key: row.get(key) for key in [
        'xgAgainst', 'xgGoalsAgainst', 'fenwickAgainst'
    ]}
    teamTriCodes = [db.session.get(Team, int(teamID)).triCode for teamID in row.get('teams').split(',')]

    obj_dict['totals'] = totals
    obj_dict['advanced'] = advanced if all([item is not None for item in advanced.values()]) else None
    obj_dict['teamTriCodes'] = teamTriCodes
    obj_dict['position'] = 'G'
    obj = GoalieLeaderboardItem(**obj_dict)
    return obj.model_dump()

def update_skater_leaderboard(season: int, gameType: int):
    with open(os.path.join(ROOT_PATH, 'sql', 'skater_leaderboard.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"season": season, "gameType": gameType}).mappings().all()
    result_rows = [dict(row) for row in query_result]
    leaderboard = [skater_row_to_object(row) for row in result_rows]

    with open(os.path.join(ROOT_PATH, 'data', 'leaderboards', f'skaters_{season}_{gameType}.json'), 'w') as f:
        json.dump(leaderboard, f)

def update_goalie_leaderboard(season: int, gameType: int):
    with open(os.path.join(ROOT_PATH, 'sql', 'goalie_leaderboard.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"season": season, "gameType": gameType}).mappings().all()
    result_rows = [dict(row) for row in query_result]

    leaderboard = []
    for row in result_rows:
        leaderboard.append(goalie_row_to_object(row))

    with open(os.path.join(ROOT_PATH, 'data', 'leaderboards', f'goalies_{season}_{gameType}.json'), 'w') as f:
        json.dump(leaderboard, f)
