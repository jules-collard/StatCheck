from app.api import bp, db
from app.api.errors import bad_request
from app.models import Team
from json import loads

from flask import request
import sqlalchemy as sa

@bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return db.get_or_404(Team, id).to_dict()

@bp.route('/teams', methods=['POST'])
def add_team():
    data = loads(request.get_json())
    print(data)
    print(type(data))
    required_cols = {'id', 'fullName', 'commonName', 'placeName'}

    if not required_cols.issubset(data.keys()):
        return bad_request(f"Missing required fields: {required_cols - required_cols.intersection(data.keys())}")
    elif db.session.scalar(sa.select(Team).where(Team.id == data['id'])):
        return bad_request("Team already in database")
    
    team = Team()
    team.from_dict(data)
    db.session.add(team)
    db.session.commit()

    return team.to_dict(), 201