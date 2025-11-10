from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.players import PlayerBase
from app.services.player_service import PlayerService

router = APIRouter(prefix='/api/players')

@router.get('/{id}')
async def get_player(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_player(id)
    
@router.post('/', status_code=status.HTTP_201_CREATED)
async def upsert_player(
    player: PlayerBase,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.add_player(player)