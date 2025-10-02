import os
import json

from sqlalchemy import text

from app import db

def update_skater_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'skater_season_records.sql'), 'r') as f:
        skater_query = f.read()

    skater_query_result = db.session.execute(text(skater_query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in skater_query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', f'skater_records_{gameType}.json'), 'w') as f:
        json.dump(results, f)

def update_goalie_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'goalie_season_records.sql'), 'r') as f:
        goalie_query = f.read()

    goalie_query_result = db.session.execute(text(goalie_query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in goalie_query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', f'goalie_records_{gameType}.json'), 'w') as f:
        json.dump(results, f)

def update_max_games():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'max_games.sql'), 'r') as f:
        query = f.read()

    query_result = db.session.execute(text(query)).mappings().all()
    max_games = [dict(row) for row in query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', 'max_games.json'), 'w') as f:
        json.dump(max_games, f)

def update_all_records():
    update_skater_records(2)
    update_skater_records(3)
    update_goalie_records(2)
    update_goalie_records(3)
    update_max_games()