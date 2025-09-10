import json
import os

from flask_cors import cross_origin
from flask import request, abort
import sqlalchemy as sa
from sqlalchemy.sql import text
from pydantic import ValidationError

from app.api import bp, db
from app.models import Player, Team

@bp.route('/players', methods=['GET'])
@cross_origin()
def get_player_list():
    players = db.session.scalars(sa.select(Player).order_by(Player.lastName.asc())).all()
    player_list_items = [p.model_dump() for player in players if (p := player.get_list_item())]
    return json.dumps(player_list_items)

@bp.route('/players/<int:id>', methods=['GET'])
@cross_origin()
def get_player(id):
    try:
        player_info = db.get_or_404(Player, id).get_player_info()
        return json.dumps(player_info.model_dump())
    except ValidationError as e:
        print(e)
        abort(406)

@bp.route('/players/<int:id>/stats', methods=['GET'])
@cross_origin()
def get_player_stats(id: int):
    player = db.get_or_404(Player, id)
    
    try:
        gameType = int(request.args.get('gameType', 2))
    except ValueError:
        abort(404)

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
        season_dict = next((d for d in analytics_results if d['season'] == row['season'] and d['teamID'] == row['teamID']), None)
        if season_dict is not None and player.position != 'G':
            row['xg'] = season_dict['xg']
            row['xgGoals'] = season_dict['xgGoals']
            row['fenwick'] = season_dict['fenwick']
        elif season_dict is not None and player.position == 'G':
            row['xgAgainst'] = season_dict['xgAgainst']
            row['xgGoalsAgainst'] = season_dict['xgGoalsAgainst']
            row['fenwickAgainst'] = season_dict['fenwickAgainst']

    teams: dict[int, Team] = {}
    for teamID in set([season["teamID"] for season in results]):
        teams[teamID] = db.session.get(Team, teamID)

    for season in results:
        season['team'] = teams[season['teamID']].get_team_info().model_dump()
        season.pop('teamID', None)

    return json.dumps(results)
