from app.api import bp, db
from app.api.errors import bad_request
from app.models import Player

from flask import request
import sqlalchemy as sa

@bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    return db.get_or_404(Player, id).to_dict()
