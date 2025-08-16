from app.api import bp, db
from flask_cors import cross_origin

from sqlalchemy.sql import text
import json, os

@bp.route('/records/skaters/<int:gameType>', methods=['GET'])
@cross_origin()
def get_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'skater_season_records.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in query_result]

    return json.dumps(results)