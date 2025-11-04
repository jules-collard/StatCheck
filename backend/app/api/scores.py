import re
from datetime import datetime
import pytz

import requests
from flask_cors import cross_origin
from flask import abort
from pydantic import ValidationError

from app.api import bp
from app.api.api_models import GameDetails, GameList

@bp.route('/scores/<date>', methods=['GET'])
@cross_origin()
def get_scores(date: str):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        abort(400)

    response = requests.get(f'http://api-web.nhle.com/v1/score/{date}')
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        abort(400)

    data = response.json()
    try:
        games = data.get('games')
        for game in games:
            game['startTimeEastern'] = pytz.timezone('UTC').localize(datetime.strptime(game.get('startTimeUTC'), "%Y-%m-%dT%H:%M:%SZ")).astimezone(pytz.timezone('Canada/Eastern')).strftime("%H:%M")
        games = [GameDetails(**game) for game in games]
        gamelist = GameList(games=games)
        return gamelist.model_dump().get('games')
    except (KeyError, ValidationError):
        abort(500)