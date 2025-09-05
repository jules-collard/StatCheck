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

    path_prefix = 'goalie' if player.position == 'G' else 'skater'

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', f'{path_prefix}_season_totals.sql')) as f:
        query = f.read()

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', f'{path_prefix}_season_analytics.sql')) as f:
        analytics_query = f.read()

    query_result = db.session.execute(text(query), {"playerID": id, "gameType": gameType}).mappings().all()
    analytics_query_result = db.session.execute(text(analytics_query), {"playerID": id, "gameType": gameType}).mappings().all()
    
    results = [dict(row) for row in query_result]
    analytics_results = [dict(row) for row in analytics_query_result]

    for row in results:
        season_dict = next((d for d in analytics_results if d['season'] == row['season']), None)
        if season_dict is not None and player.position != 'G':
            row['xg'] = season_dict['xg']
            row['actualGoals'] = season_dict['actualGoals']
            row['actualShotAttempts'] = season_dict['actualShotAttempts']
        elif season_dict is not None and player.position == 'G':
            row['xgAgainst'] = season_dict['xgAgainst']
            row['actualGoalsAgainst'] = season_dict['actualGoalsAgainst']
            row['actualShotsAgainst'] = season_dict['actualShotsAgainst']

    teams = {}
    for teamID in set([season["teamID"] for season in results]):
        teams[teamID] = db.session.get(Team, teamID).to_dict()

    for season in results:
        season['team'] = teams[season['teamID']]
        season.pop('teamID', None)

    return json.dumps(results)
