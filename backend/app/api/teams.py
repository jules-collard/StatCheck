from app.api import bp, db
from app.api.errors import bad_request
from app.models import Team
from json import loads

from flask import request
import sqlalchemy as sa

@bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return db.get_or_404(Team, id).to_dict()
