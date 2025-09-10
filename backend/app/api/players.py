import json
import os

from flask_cors import cross_origin
from flask import request, abort
import sqlalchemy as sa
from sqlalchemy.sql import text
from pydantic import ValidationError

from app.api import bp, db
from app.models import Player, Team
from app.api.api_models import SkaterStats, SkaterShooting, SkaterTotals, GoalieStats, GoalieAdvanced, GoalieTotals

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

    if player.position != 'G':
        return get_skater_stats(id, gameType)
    else:
        return get_goalie_stats(id, gameType)


def get_skater_stats(id: int, gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'skater_season_totals.sql')) as f:
        totals_query = f.read()

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'skater_season_shooting.sql')) as f:
        shooting_query = f.read()

    totals_query_result = db.session.execute(text(totals_query), {"playerID": id, "gameType": gameType}).mappings().all()
    shooting_query_result = db.session.execute(text(shooting_query), {"playerID": id, "gameType": gameType}).mappings().all()
    
    totals = [dict(row) for row in totals_query_result]
    shooting = [dict(row) for row in shooting_query_result]

    stats: list[SkaterStats] = []

    for total in totals:
        season = total.pop('season')
        teamID = total.pop('teamID')
        season_totals = SkaterTotals(**total)
        
        season_stats = SkaterStats(
            playerID=id,
            season=season,
            teamTriCode=db.session.get(Team, teamID).triCode,
            totals=season_totals
        )

        if season_shooting := next((s for s in shooting if all([s.get('season') == season, s.get('teamID') == teamID])), None):
            season_shooting.pop('season')
            season_shooting.pop('teamID')
            season_stats.shooting = SkaterShooting(**season_shooting)

        stats.append(season_stats.model_dump())

    return json.dumps(stats)

def get_goalie_stats(id: int, gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'goalie_season_totals.sql')) as f:
        totals_query = f.read()

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../sql', 'goalie_season_advanced.sql')) as f:
        advanced_query = f.read()

    totals_query_result = db.session.execute(text(totals_query), {"playerID": id, "gameType": gameType}).mappings().all()
    advanced_query_result = db.session.execute(text(advanced_query), {"playerID": id, "gameType": gameType}).mappings().all()
    
    totals = [dict(row) for row in totals_query_result]
    advanced = [dict(row) for row in advanced_query_result]

    stats: list[GoalieStats] = []

    for total in totals:
        season = total.pop('season')
        teamID = total.pop('teamID')
        season_totals = GoalieTotals(**total)
        
        season_stats = GoalieStats(
            playerID=id,
            season=season,
            teamTriCode=db.session.get(Team, teamID).triCode,
            totals=season_totals
        )

        if season_advanced := next((s for s in advanced if all([s.get('season') == season, s.get('teamID') == teamID])), None):
            season_advanced.pop('season')
            season_advanced.pop('teamID')
            season_stats.advanced = GoalieAdvanced(**season_advanced)

        stats.append(season_stats.model_dump())

    return json.dumps(stats)