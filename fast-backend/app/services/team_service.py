from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
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
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def get_team(self, id: int):
        team: Team | None = await self.session.get(Team, id)
        if team is None:
            raise HTTPException(404, detail="Team not found")
        else:
            return await self.return_team(team)
    
    async def add_team(self, team: TeamBase):
        data = team.model_dump()
        teamObj = Team(**data)
        self.session.add(teamObj)
        return await self.return_team(teamObj)
    
    async def upsert_team(self, team: TeamBase):
        data = team.model_dump()

        stmt = insert(Team).values(**data).returning(Team).on_conflict_do_nothing(index_elements=[Team.id])
        result = await self.session.execute(stmt)
        newTeam = result.scalar_one()
        return await self.return_team(newTeam)
    
    async def delete_team(self, id: int):
        team: Team | None = await self.session.get(Team, id)
        if team is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        else:
            await self.session.delete(team)
            return