from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, literal_column
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.models.players import SkaterLeaderboardItem, SkaterTotals, SkaterShooting, SkaterOnIce
from app.models.players import GoalieLeaderboardItem, GoalieTotals, GoalieAdvanced
from app.db.schema import Team

class LeaderboardService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_skater_leaderboard(self, season: int, gameType: int):
        q = (select(literal_column('*'))).select_from(text('skater_stats')).where('''"season" = :season AND "gameType" = :game_type''')
        result = await self.session.execute(q, {'season': season, 'game_type': gameType})
        leaderboardItems: List[SkaterLeaderboardItem] = []
        for row in result.all():
            leaderboardItems.append(await self.row_to_skater_leaderboard(row))

        return [item.model_dump() for item in leaderboardItems]
    
    async def get_goalie_leaderboard(self, season: int, gameType: int):
        q = (select(literal_column('*'))).select_from(text('goalie_stats')).where('''"season" = :season AND "gameType" = :game_type''')
        result = await self.session.execute(q, {'season': season, 'game_type': gameType})
        leaderboardItems: List[GoalieLeaderboardItem] = []
        for row in result.all():
            leaderboardItems.append(await self.row_to_goalie_leaderboard(row))

        return [item.model_dump() for item in leaderboardItems]

    async def get_team_tricodes(self, ids: List[int]):
        return await self.session.scalars(select(Team.triCode).where(Team.id.in_(ids)))

    async def row_to_skater_leaderboard(self, row: List) -> SkaterLeaderboardItem:
        triCodes = await self.get_team_tricodes(row[7])
        try:
            return SkaterLeaderboardItem(
                playerID=row[2],
                fullName=row[3] + ' ' + row[4],
                position=row[5],
                isActive=row[6],
                teamTriCodes=triCodes,
                qualified=row[8],
                shotsQualified=row[9],
                totals=SkaterTotals(
                    gamesPlayed=row[10],
                    goals=row[11],
                    assists=row[12],
                    plusMinus=row[13],
                    penaltyMinutes=row[14],
                    hits=row[15],
                    sog=row[16],
                    blocks=row[17],
                    avgTOI=row[18]
                ),
                shooting=SkaterShooting(
                    xg=row[19],
                    xgGoals=row[20],
                    fenwick=row[21]
                ),
                onIce=SkaterOnIce(
                    onIceShootingPct=row[22],
                    fenwickFor=row[23],
                    fenwickAgainst=row[24],
                    corsiFor=row[25],
                    corsiAgainst=row[26],
                    xgFor=row[27],
                    xgAgainst=row[28],
                    oZoneStarts=row[29],
                    nZoneStarts=row[30],
                    dZoneStarts=row[31]
                )
            )
        except IndexError:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error reading row")
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def row_to_goalie_leaderboard(self, row: List) -> GoalieLeaderboardItem:
        triCodes = await self.get_team_tricodes(row[6])
        try:
            return GoalieLeaderboardItem(
                playerID=row[2],
                fullName=row[3] + ' ' + row[4],
                position='G',
                isActive=row[5],
                teamTriCodes=triCodes,
                qualified=row[7],
                totals=GoalieTotals(
                    gamesPlayed=row[8],
                    gamesStarted=row[9],
                    wins=row[10],
                    losses=row[11],
                    goalsAgainst=row[12],
                    goalsAgainstAvg=row[13],
                    savePct=row[14],
                    evenStrengthSavePct=row[15],
                    powerPlaySavePct=row[16]
                ),
                advanced=GoalieAdvanced(
                    xgAgainst=row[17],
                    xgGoalsAgainst=row[18],
                    fenwickAgainst=row[19]
                )
            )
        except IndexError:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error reading row")
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())