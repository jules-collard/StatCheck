import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytz

import requests
from flask_cors import cross_origin
from flask import abort
from pydantic import ValidationError

from app.api import bp
from app.api.api_models import GameDetails, GameList

@cross_origin()
@bp.route('/scores/<date>', methods=['GET'])
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
            game['startTimeEastern'] = pytz.timezone('UTC').localize(datetime.strptime(game.get('startTimeUTC'), "%Y-%m-%dT%H:%M:%SZ")).astimezone(pytz.timezone('Canada/Eastern')).strftime("%Y-%m-%dT%H:%M:%S")
        games = [GameDetails(**game) for game in games]
        gamelist = GameList(games=games)
        return gamelist.model_dump().get('games')
    except KeyError or ValidationError:
        abort(500)