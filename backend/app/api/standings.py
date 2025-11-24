import json

import requests
from flask_cors import cross_origin
from flask import abort
from pydantic import ValidationError

from app.api import bp
from app.api.api_models import StandingsItem

@bp.route('/standings', methods=['GET'])
@cross_origin()
def get_league_standings():
    response = requests.get('https://api-web.nhle.com/v1/standings/now')
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        abort(400)

    data = response.json()

    try:
        standings = data.get('standings')
        for team in standings:
            team['teamAbbrev'] = team.get('teamAbbrev').get('default')

        standings = [StandingsItem(**team) for team in standings]
        return json.dumps([item.model_dump() for item in standings])
    except (KeyError, ValidationError):
        abort(500)

