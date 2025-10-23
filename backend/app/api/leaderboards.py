import os
import json

from flask_cors import cross_origin
from flask import request, abort

import app
from app.api import bp

@bp.route('/leaderboards/<int:season>/skaters', methods=['GET'])
@cross_origin()
def get_skater_leaderboards(season: int, gameType: int = 2):
    try:
        gameType = int(request.args.get('gameType', 2))
        if gameType not in [2,3]:
            raise ValueError
        with open(os.path.join(app.ROOT_PATH, 'data', 'leaderboards', f'skaters_{season}_{gameType}.json')) as f:
            leaderboard = json.load(f)
            return json.dumps(leaderboard)
    except ValueError:
        abort(400)
    except FileNotFoundError:
        abort(404)

@bp.route('/leaderboards/<int:season>/goalies', methods=['GET'])
@cross_origin()
def get_goalie_leaderboards(season: int, gameType: int = 2):
    try:
        gameType = int(request.args.get('gameType', 2))
        if gameType not in [2,3]:
            raise ValueError
        with open(os.path.join(app.ROOT_PATH, 'data', 'leaderboards', f'goalies_{season}_{gameType}.json')) as f:
            leaderboard = json.load(f)
            return json.dumps(leaderboard)
    except ValueError:
        abort(400)
    except FileNotFoundError:
        abort(404)