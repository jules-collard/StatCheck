from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import ValidationError

from app.db.schema import SkaterAppearance, GoalieAppearance
from app.models.appearances import SkaterAppearanceBase, GoalieAppearanceBase


class AppearanceService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_skater_appearances_exist(self, gameID: int):
        stmt = select(SkaterAppearance).where(SkaterAppearance.gameID == gameID)
        skaters = await self.session.scalars(stmt)
        if len(skaters.all()) > 0:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='Skater appearances already in database')
        
    async def check_goalie_appearances_exist(self, gameID: int):
        stmt = select(GoalieAppearance).where(GoalieAppearance.gameID == gameID)
        goalies = await self.session.scalars(stmt)
        if len(goalies.all()) > 0:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='Goalie appearances already in database')
        
    async def insert_skater_appearances(self, gameID: int, apps: List[SkaterAppearanceBase]):
        await self.check_skater_appearances_exist(gameID)
        try:
            app_objs = [SkaterAppearance(**skater.model_dump()) for skater in apps]
            self.session.add_all(app_objs)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def insert_goalie_appearances(self, gameID: int, apps: List[GoalieAppearanceBase]):
        await self.check_goalie_appearances_exist(gameID)
        try:
            app_objs = [GoalieAppearance(**goalie.model_dump()) for goalie in apps]
            self.session.add_all(app_objs)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())