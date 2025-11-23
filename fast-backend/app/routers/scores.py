from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession

from app.db.database import get_session
from app.core.external import get_http_session
from app.services.live_service import LiveService

router = APIRouter(prefix='/scores')

@router.get('/{date}', status_code=status.HTTP_200_OK)
async def get_scores(
    date: str,
    session: AsyncSession = Depends(get_session),
    http_session: ClientSession = Depends(get_http_session)
):
    service = LiveService(session, http_session)
    return await service.get_scores(date)