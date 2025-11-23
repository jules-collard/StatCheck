import re
from datetime import datetime

import pytz
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.external import fetch
from app.models.games import GameDetails

class LiveService:

    def __init__(self, session: AsyncSession, http_session: ClientSession):
        self.session = session
        self.http_session = http_session

    async def get_scores(self, date: str):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
        
        try:
            data = await fetch(self.http_session, f'http://api-web.nhle.com/v1/score/{date}')
            games = data.get('games')
            for game in games:
                game['startTimeEastern'] = pytz.timezone('UTC').localize(datetime.strptime(game.get('startTimeUTC'), "%Y-%m-%dT%H:%M:%SZ")).astimezone(pytz.timezone('Canada/Eastern')).strftime("%H:%M")
            return [GameDetails(**game).model_dump() for game in games]
        except AssertionError:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Data not available")
        except KeyError or ValidationError:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process games")


# def get_scores(date: str):
#     if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
#         abort(400)

#     response = requests.get(f'http://api-web.nhle.com/v1/score/{date}')
#     try:
#         response.raise_for_status()
#     except requests.exceptions.HTTPError:
#         abort(400)

#     data = response.json()
#     try:
#         games = data.get('games')
#         for game in games:
#             game['startTimeEastern'] = pytz.timezone('UTC').localize(datetime.strptime(game.get('startTimeUTC'), "%Y-%m-%dT%H:%M:%SZ")).astimezone(pytz.timezone('Canada/Eastern')).strftime("%H:%M")
#         games = [GameDetails(**game) for game in games]
#         gamelist = GameList(games=games)
#         return gamelist.model_dump().get('games')
#     except (KeyError, ValidationError):
#         abort(500)