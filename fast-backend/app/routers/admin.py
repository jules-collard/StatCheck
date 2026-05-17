from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_credentials
from app.db.database import get_session
from app.services.admin_service import AdminService

router = APIRouter(prefix='/admin')

@router.get('/healthcheck', status_code=status.HTTP_200_OK)
def return_check():
    return {"status": "healthy"}

@router.get('/init-views', status_code=status.HTTP_200_OK, dependencies=[Depends(check_credentials)])
async def initialise_views(
    session: AsyncSession = Depends(get_session)
):
    service = AdminService(session)
    await service.create_skater_stats_view()
    await service.create_goalie_stats_view()

@router.get('/refresh-views', status_code=status.HTTP_200_OK, dependencies=[Depends(check_credentials)])
async def refresh_views(
    session: AsyncSession = Depends(get_session)
):
    service = AdminService(session)
    await service.refresh_views()