from app.api import bp, db
from app.models import Player
from flask_cors import cross_origin

from sqlalchemy.sql import text
import json

@bp.route('/players/<int:id>', methods=['GET'])
@cross_origin()
def get_player(id):
    return db.get_or_404(Player, id).to_dict()

@bp.route('/players/<int:id>/stats', methods=['GET'])
@cross_origin()
def get_player_stats(id):
    db.get_or_404(Player, id)
    query = f"SELECT * FROM season_stats WHERE playerID == {id}"
    query_result = db.session.execute(text(query)).mappings().all()
    results = [dict(row) for row in query_result]

    return json.dumps(results)
