from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_credentials
from app.db.database import get_session
from app.models.teams import TeamBase
from app.services.team_service import TeamService

router = APIRouter(prefix='/teams')

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_team(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = TeamService(session)
    return await service.get_team(id)

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_team(
    team: TeamBase,
    session: AsyncSession = Depends(get_session)
):
    service = TeamService(session)
    if await service.team_exists(team.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Team already exists")
    
    return await service.add_team(team)

@router.put('/', status_code=status.HTTP_200_OK, dependencies=[Depends(check_credentials)])
async def put_team(
    team: TeamBase,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    service = TeamService(session)
    if not await service.team_exists(team.id):
        response.status_code = status.HTTP_201_CREATED
        return await service.add_team(team)
    else:
        return await service.get_team(team.id)
    
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(check_credentials)])
async def delete_team(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = TeamService(session)
    return await service.delete_team(id)
        