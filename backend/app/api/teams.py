from app.api import bp, db
from app.models import Team
from flask_cors import cross_origin

@bp.route('/teams/<int:id>', methods=['GET'])
@cross_origin()
def get_team(id):
    return db.get_or_404(Team, id).to_dict()
