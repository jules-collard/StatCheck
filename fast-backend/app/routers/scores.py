from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

router = APIRouter(prefix='/scores')

@router.get('/{date}', status_code=status.HTTP_200_OK)
async def get_scores(
    date: str,
    session: AsyncSession = Depends(get_session)
):
    pass