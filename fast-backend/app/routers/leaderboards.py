from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

router = APIRouter(prefix='/leaderboards')

@router.get('/{season}/skaters', status_code=status.HTTP_200_OK)
async def get_skater_leaderboard(
    season: int,
    session: AsyncSession = Depends(get_session)
):
    pass

@router.get('/{season}/goalies', status_code=status.HTTP_200_OK)
async def get_goalie_leaderboard(
    season: int,
    session: AsyncSession = Depends(get_session)
):
    pass