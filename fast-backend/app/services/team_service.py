from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from fastapi import HTTPException, status

from app.db.schema import Team
from app.models.teams import TeamBase

class TeamService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def team_exists(self, id: int):
        return await self.session.get(Team, id) is not None
    
    async def return_team(self, team: Team):
        try:
            teamObj: TeamBase = team.to_read()
            return teamObj.model_dump()
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
    async def add_team(self, team: TeamBase):
        data = team.model_dump()
        teamObj = Team(**data)
        self.session.add(teamObj)
        return await self.return_team(teamObj)