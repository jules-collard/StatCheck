from app.api import bp, db
from app.models import Player
from flask_cors import cross_origin

from sqlalchemy.sql import text
import json, os

@bp.route('/players/<int:id>', methods=['GET'])
@cross_origin()
def get_player(id):
    return db.get_or_404(Player, id).to_dict()

@bp.route('/players/<int:id>/stats', methods=['GET'])
@cross_origin()
def get_player_stats(id):
    db.get_or_404(Player, id)

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'player_season_totals.sql')) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"playerID": id, "gameType": 2}).mappings().all()
    results = [dict(row) for row in query_result]

    return json.dumps(results)
