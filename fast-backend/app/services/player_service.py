from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.db.schema import Player, Award
from app.models.players import PlayerBase, PlayerRead

class PlayerService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_player(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if player is None:
            raise HTTPException(404, detail="Player not found")
        else:
            data = await player.to_dict()
            try:
                return PlayerRead(**data).model_dump()
            except ValidationError as e:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        
    async def add_player(self, player: PlayerBase):
        if await self.session.get(Player, player.id) is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Player already exists")
        
        data = player.model_dump()
        awards = data.pop('awards', [])
        data['birthDate'] = datetime.strptime(data.get('birthDate', ''), '%Y-%m-%d').date()
        
        playerObj = Player(**data)
        
        for award in awards:
            awardObj = Award(**award)
            playerObj.awards.append(awardObj)
        
        self.session.add(playerObj)
        return {"message" : "success"}