from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Player

router = APIRouter()

@router.get('/players/{id}')
async def get_player(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    player: Player | None = session.get(Player, id)
    if player is None:
        raise HTTPException(404, detail="Player not found")
    else:
        return player.to_dict()
    
@router.put('/players', response_model=Player, status_code=200)
async def upsert_player(
    player: Player,
    session: AsyncSession = Depends(get_session)
):
    session.merge(player)