from app.api import bp, db
from app.models import Player, Team
from flask_cors import cross_origin
from flask import request

from sqlalchemy.sql import text
import sqlalchemy as sa
import json, os

@bp.route('/players', methods=['GET'])
@cross_origin()
def get_all_players():
    players = db.session.scalars(sa.select(Player).order_by(Player.lastName.asc())).all()
    players_dict = [{
        'id':player.id,
        'fullName': f"{player.firstName} {player.lastName}",
        'position': player.position,
        'teamTriCode': player.team.triCode if player.team else None,
        'headshot': player.headshot}
        for player in players
    ]
    return json.dumps(players_dict)

@bp.route('/players/<int:id>', methods=['GET'])
@cross_origin()
def get_player(id):
    return db.get_or_404(Player, id).to_dict()

@bp.route('/players/<int:id>/stats', methods=['GET'])
@cross_origin()
def get_player_stats(id):
    player = db.get_or_404(Player, id)
    gameType = int(request.args.get('gameType', 2))

    querypath = 'goalie_season_totals.sql' if player.position == 'G' else 'player_season_totals.sql'

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', querypath)) as f:
        query = f.read()

    query_result = db.session.execute(text(query), {"playerID": id, "gameType": gameType}).mappings().all()
    results = [dict(row) for row in query_result]
    
    teams = {}
    for teamID in set([season["teamID"] for season in results]):
        teams[teamID] = db.session.get(Team, teamID).to_dict()

    for season in results:
        season['team'] = teams[season['teamID']]
        season.pop('teamID', None)

    return json.dumps(results)
