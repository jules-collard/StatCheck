from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.players import PlayerBase
from app.db.schema import Player, Award

router = APIRouter(prefix='/api/players')

@router.get('/{id}')
async def get_player(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    player: Player | None = session.get(Player, id)
    if player is None:
        raise HTTPException(404, detail="Player not found")
    else:
        return player.to_dict()
    
@router.put('/', status_code=status.HTTP_201_CREATED)
async def upsert_player(
    player: PlayerBase,
    session: AsyncSession = Depends(get_session)
):
    attributes = player.model_dump()
    awards = attributes.pop('awards', [])
    attributes['birthDate'] = datetime.strptime(attributes.get('birthDate'), '%Y-%m-%d').date()
    
    playerObj = Player(**attributes)
    for award in awards:
        awardObj = Award(**award)
        playerObj.awards.append(awardObj)
    session.add(playerObj)
    return {"message" : "success"}