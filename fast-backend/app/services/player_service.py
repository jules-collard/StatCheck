from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.db.schema import Player, Award, Team
from app.models.players import PlayerBase, PlayerRead, PlayerListItem, AwardBase

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
        
