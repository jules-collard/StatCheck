from app.api import bp, db
from app.models import Player
from flask_cors import cross_origin

@bp.route('/players/<int:id>', methods=['GET'])
@cross_origin()
def get_player(id):
    return db.get_or_404(Player, id).to_dict()
