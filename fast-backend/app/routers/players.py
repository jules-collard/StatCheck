from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.schema import Player
from app.models.players import PlayerBase
from app.services.player_service import PlayerService

router = APIRouter(prefix='/api/players')

@router.get('/info/{id}', status_code=status.HTTP_200_OK)
async def get_player(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_player(id)

@router.get('/all/ids', status_code=status.HTTP_200_OK)
async def get_all_ids(
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_all_ids()
    
@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_player(
    player: PlayerBase,
    session: AsyncSession = Depends(get_session)
):
    if await session.get(Player, player.id) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Player already exists")
    
    service = PlayerService(session)
    return await service.add_player(player)

@router.put('/', status_code=200)
async def put_player(
    player: PlayerBase,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    service = PlayerService(session)
    if not await service.player_exists(player.id):
        response.status_code = status.HTTP_201_CREATED
    return await service.upsert_player(player)