from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(prefix='/leaderboards')

@router.get('/{season}/skaters', status_code=status.HTTP_200_OK)
async def get_skater_leaderboard(
    season: int,
    gameType: int = 2,
    session: AsyncSession = Depends(get_session)
):
    service = LeaderboardService(session)
    return await service.get_skater_leaderboard(season, gameType)
    

@router.get('/{season}/goalies', status_code=status.HTTP_200_OK)
async def get_goalie_leaderboard(
    season: int,
    gameType: int = 2,
    session: AsyncSession = Depends(get_session)
):
    service = LeaderboardService(session)
    return await service.get_goalie_leaderboard(season, gameType)