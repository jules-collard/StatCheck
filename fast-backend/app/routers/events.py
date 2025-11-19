from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.event_service import EventService
from app.models.events import EventPatchXG

router = APIRouter(prefix='/events')

@router.patch('/', status_code=status.HTTP_202_ACCEPTED)
async def patch_event_xg(
    shots: List[EventPatchXG],
    session: AsyncSession = Depends(get_session)
):
    service = EventService(session)
    await service.update_xg(shots)