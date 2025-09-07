import json
import os

from flask_cors import cross_origin
from sqlalchemy.sql import text

from app.api import bp, db

@bp.route('/records/skaters/<int:gameType>', methods=['GET'])
@cross_origin()
def get_skater_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'skater_season_records.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in query_result]

    return json.dumps(results)

@bp.route('/records/goalies/<int:gameType>', methods=['GET'])
@cross_origin()
def get_goalie_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'goalie_season_records.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in query_result]

    return json.dumps(results)