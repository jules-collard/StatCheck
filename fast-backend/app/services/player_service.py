from datetime import datetime
from typing import List

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.db.schema import Player, Award, Team
from app.models.players import PlayerBase, PlayerRead, PlayerListItem, AwardBase
from app.models.players import SkaterStats, SkaterTotals, SkaterShooting, SkaterOnIce
from app.models.players import GoalieStats, GoalieTotals, GoalieAdvanced

class PlayerService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def player_exists(self, id: int):
        return await self.session.get(Player, id) is not None
    
    async def return_player(self, player: Player):
        try:
            playerObj: PlayerRead = await player.to_read()
            return playerObj.model_dump()
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())

    async def get_player(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if player is None:
            raise HTTPException(404, detail="Player not found")
        else:
            return await self.return_player(player)
        
    async def get_list_item(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if player is None:
            raise HTTPException(404, detail="Player not found")
        else:
            try:
                playerObj: PlayerListItem = await player.to_list_item()
                return playerObj.model_dump()
            except ValidationError as e:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
            
    async def get_all_ids(self):
        result = await self.session.execute(select(Player.id))
        return result.scalars().all()
    
    async def get_all_list_items(self):
        stmt = (select(Player.id, Player.firstName, Player.lastName, Player.isActive, Player.position, Team.triCode, Player.headshot)
                .outerjoin(Team)
                .order_by(Player.lastName))
        result = await self.session.execute(stmt)
        return [PlayerListItem(
            id=row.id,
            fullName=f"{row.firstName} {row.lastName}",
            isActive=row.isActive,
            position=row.position,
            teamTriCode=row.triCode,
            headshot=row.headshot).model_dump() for row in result]
        
    async def insert_player(self, player: PlayerBase):
        data = player.model_dump()
        awards = data.pop('awards', [])
        data['birthDate'] = datetime.strptime(data.get('birthDate', ''), '%Y-%m-%d').date()
        
        try:
            stmt = insert(Player).values(data)
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
        
        for award in awards:
            awardObj = AwardBase(**award)
            await self.upsert_award(awardObj)
    
    async def upsert_player(self, player: PlayerBase):
        data = player.model_dump()
        awards = data.pop('awards', [])
        data['birthDate'] = datetime.strptime(data.get('birthDate', ''), '%Y-%m-%d').date()

        for award in awards:
            awardObj = AwardBase(**award)
            await self.upsert_award(awardObj)

        stmt = insert(Player).values(**data)
        update_stmt = (stmt.on_conflict_do_update(
            index_elements=[Player.id],
            set_=dict(
                isActive=stmt.excluded.isActive,
                currentTeamID=stmt.excluded.currentTeamID,
                sweaterNumber=stmt.excluded.sweaterNumber,
                position=stmt.excluded.position,
                headshot=stmt.excluded.headshot,
                heightInInches=stmt.excluded.heightInInches,
                heightInCentimeters=stmt.excluded.heightInCentimeters,
                weightInPounds=stmt.excluded.weightInPounds,
                weightInKilograms=stmt.excluded.weightInKilograms,
                inHHOF=stmt.excluded.inHHOF,
            )
        ))
        try:
            await self.session.execute(update_stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    async def delete_player(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if player is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        else:
            await self.session.delete(player)

    async def upsert_award(self, award: AwardBase):
        stmt = (insert(Award)
                .values(**award.model_dump())
                .on_conflict_do_nothing(constraint="awards_constraint"))
        try:
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
        
    async def get_player_stats(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if not player:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Player not in database")
        
        if player.position == 'G':
            q = f"""SELECT * FROM goalie_stats WHERE "playerID" = {player.id}"""
        else:
            q = f"""SELECT * FROM skater_stats WHERE "playerID" = {player.id}"""
        result = await self.session.execute(text(q))
        stats: List[SkaterStats | GoalieStats] = []
        for row in result.all():
            if player.position == 'G':
                stats.append(await self.row_to_goalie_stats(row))
            else:
                stats.append(await self.row_to_skater_stats(row))
        return [season.model_dump() for season in stats]

    async def get_team_tricodes(self, ids: List[int]):
        return await self.session.scalars(select(Team.triCode).where(Team.id.in_(ids)))
    
    async def row_to_skater_stats(self, row: List) -> SkaterStats:
        triCodes = await self.get_team_tricodes(row[7])
        try:
            return SkaterStats(
                playerID=row[2],
                season=row[0],
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
                onice=SkaterOnIce(
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
        
    async def row_to_goalie_stats(self, row: List) -> GoalieStats:
        triCodes = await self.get_team_tricodes(row[6])
        try:
            return GoalieStats(
                playerID=row[2],
                season=row[0],
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