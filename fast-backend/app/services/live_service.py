import re
from datetime import datetime

import pytz
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.external import fetch
from app.models.games import GameDetails, TeamStandingsItem

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
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Data not available")
        except (KeyError, ValidationError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process games")
        
    async def get_standings(self):
        try:
            data = await fetch(self.http_session, 'http://api-web.nhle.com/v1/standings/now')
            standings = data.get('standings')
            for team in standings:
                team['teamAbbrev'] = team.get('teamAbbrev').get('default')
            return [TeamStandingsItem(**team).model_dump() for team in standings]
        except AssertionError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Data not available")
        except (KeyError, ValidationError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process games")
