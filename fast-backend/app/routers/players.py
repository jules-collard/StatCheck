from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.schema import Player
from app.models.players import PlayerBase
from app.services.player_service import PlayerService

router = APIRouter(prefix='/api/players')

@router.get('/{id}/info', status_code=status.HTTP_200_OK)
async def get_player(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_player(id)

@router.get('/{id}/list-item', status_code=status.HTTP_200_OK)
async def get_player_list_item(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_list_item(id)

@router.get('/all/ids', status_code=status.HTTP_200_OK)
async def get_all_ids(
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_all_ids()

@router.get('/all/list-items', status_code=status.HTTP_200_OK)
async def get_all_list_items(
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    return await service.get_all_list_items()
    
@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_player(
    player: PlayerBase,
    session: AsyncSession = Depends(get_session)
):
    service = PlayerService(session)
    if await service.player_exists(player.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Player already exists")
    
    return await service.add_player(player)

@router.put('/', status_code=status.HTTP_200_OK)
async def put_player(
    player: PlayerBase,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    service = PlayerService(session)
    if not await service.player_exists(player.id):
        response.status_code = status.HTTP_201_CREATED
    return await service.upsert_player(player)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_player(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    service = PlayerService(session)
    return await service.delete_player(id)