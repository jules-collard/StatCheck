from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_credentials
from app.db.database import get_session
from app.models.games import GameBase
from app.models.events import EventTypeBase, EventBase
from app.models.appearances import SkaterAppearanceBase, GoalieAppearanceBase
from app.models.shifts import ShiftBase, SplitShiftBase
from app.services.game_service import GameService
from app.services.event_service import EventService
from app.services.appearance_service import AppearanceService
from app.services.shift_service import ShiftService

router = APIRouter(prefix='/games')

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_game(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    return await service.get_game(id)

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_game(
    game: GameBase,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    if await service.game_exists(game.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Game already exists')
    return service.add_game(game)

@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(check_credentials)])
async def delete_game(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    return await service.delete_game(id)

@router.post('/event-types', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_event_types(
    event_types: List[EventTypeBase],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return service.add_event_types(event_types)

@router.post('/{id}/events', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_game_events(
    id: int,
    events: List[EventBase],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return await service.insert_events(id, events)

@router.get('/{id}/events', status_code=status.HTTP_200_OK)
async def get_game_events(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return await service.get_events(id)

@router.post('/{id}/skater-apps', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_skater_appearances(
    id: int,
    apps: List[SkaterAppearanceBase],
    session: AsyncSession = Depends(get_session)
):
    service = AppearanceService(session)
    return await service.insert_skater_appearances(id, apps)

@router.post('/{id}/goalie-apps', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_goalie_appearances(
    id: int,
    apps: List[GoalieAppearanceBase],
    session: AsyncSession = Depends(get_session)
):
    service = AppearanceService(session)
    return await service.insert_goalie_appearances(id, apps)

@router.post('/{id}/shifts', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_shifts(
    id: int,
    shifts: List[ShiftBase],
    session: AsyncSession = Depends(get_session)
):
    service = ShiftService(session)
    return await service.insert_shifts(id, shifts)

@router.get('/{id}/shifts', status_code=status.HTTP_200_OK)
async def get_game_shifts(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    service = ShiftService(session)
    return await service.get_shifts(id)

@router.post('/{id}/split-shifts', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_credentials)])
async def post_split_shifts(
    id: int,
    splitshifts: List[SplitShiftBase],
    session: AsyncSession = Depends(get_session)
):
    service = ShiftService(session)
    return await service.insert_split_shifts(id, splitshifts)