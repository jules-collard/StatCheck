from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.teams import TeamBase
from app.services.team_service import TeamService

router = APIRouter(prefix='/api/teams')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_team(
    team: TeamBase,
    session: AsyncSession = Depends(get_session)
):
    service = TeamService(session)
    if await service.team_exists(team.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Team already exists")
    
    return await service.add_team(team)