from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.games import GameBase
from app.models.events import EventTypeBase, EventBase
from app.db.database import get_session
from app.services.game_service import GameService
from app.services.event_service import EventService

router = APIRouter(prefix='/games')

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_game(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    return await service.get_game(id)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_game(
    game: GameBase,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    if await service.game_exists(game.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Game already exists')
    return service.add_game(game)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_game(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    return await service.delete_game(id)

@router.post('/event-types', status_code=status.HTTP_201_CREATED)
async def post_event_types(
    event_types: List[EventTypeBase],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return service.add_event_types(event_types)

@router.post('/{id}/events', status_code=status.HTTP_201_CREATED)
async def post_game_events(
    id: int,
    events: List[EventBase],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return await service.insert_events(id, events)
