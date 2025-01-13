from app.api import bp, db
from app.api.errors import bad_request
from app.models import Player

from flask import request
import sqlalchemy as sa

@bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    return db.get_or_404(Player, id).to_dict()

@bp.route('/players', methods=['POST'])
def add_player():
    data = request.get_json()
    required_cols = {'id', 'isActive', 'currentTeamID', 'firstName', 'lastName', 'position', 'birthDate', 'shootsCatches'}
    
    if not required_cols.issubset(data.keys()):
        return bad_request(f"Missing required fields: {required_cols - required_cols.intersection(data.keys())}")
    elif db.session.scalar(sa.select(Player).where(Player.id == data['id'])):
        return bad_request("Player already in database")
    
    player = Player()
    player.from_dict(data)
    db.session.add(player)
    db.session.commit()

    return player.to_dict(), 201
