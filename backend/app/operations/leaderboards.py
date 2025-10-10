import os
import json

from sqlalchemy import text

from app import app, db, ROOT_PATH
from app.models import Team
from app.api.api_models import SkaterLeaderboardItem

def row_to_object(row: dict):
    obj_dict = {key: row.get(key) for key in ['playerID', 'firstName', 'lastName', 'position']}
    totals = {key: row.get(key) for key in [
        'gamesPlayed', 'goals', 'assists', 'plusMinus', 'hits', 'sog', 'blocks', 'penaltyMinutes', 'avgTOI'
    ]}
    teamTriCodes = [db.session.get(Team, int(teamID)).triCode for teamID in row.get('teams').split(',')]

    obj_dict['totals'] = totals
    obj_dict['teamTriCodes'] = teamTriCodes
    obj = SkaterLeaderboardItem(**obj_dict)
    return obj.model_dump()

def update_skater_leaderboard(season: int, gameType: int):
    with open(os.path.join(ROOT_PATH, 'sql', 'skater_leaderboard.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"season": season, "gameType": gameType}).mappings().all()
    result_rows = [dict(row) for row in query_result]
    leaderboard = [row_to_object(row) for row in result_rows]

    with open(os.path.join(ROOT_PATH, 'data', 'leaderboards', f'skaters_{season}_{gameType}.json'), 'w') as f:
        json.dump(leaderboard, f)

if __name__ == "__main__":
    app.app_context().push()
    update_skater_leaderboard(20242025, 2)