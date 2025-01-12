from app.api import bp, db
from app.models import Player

@bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    # return db.get_or_404(Player, id).to_dict()
    return f"Request received {id}"