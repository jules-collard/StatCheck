from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import check_credentials
from app.db.database import get_session
from app.services.event_service import EventService
from app.models.events import EventPatchXG, EventReadShift

router = APIRouter(prefix='/events')

@router.patch('/', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_credentials)])
async def patch_event_xg(
    shots: List[EventPatchXG],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    await service.update_xg(shots)

@router.get('/', response_model=List[EventReadShift],status_code=status.HTTP_200_OK)
async def get_events_from_shift(
    gameID: int,
    period: int,
    startTimeSec: int,
    endTimeSec: int,
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    return await service.get_events_shift(gameID, period, startTimeSec, endTimeSec)