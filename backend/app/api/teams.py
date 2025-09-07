from flask_cors import cross_origin

from app.api import bp, db
from app.models import Team

@bp.route('/teams/<int:id>', methods=['GET'])
@cross_origin()
def get_team(id):
    return db.get_or_404(Team, id).to_dict()
