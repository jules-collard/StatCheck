from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.schema import Player

class PlayerService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_player(self, id: int):
        player: Player | None = await self.session.get(Player, id)
        if player is None:
            raise HTTPException(404, detail="Player not found")
        else:
            return await player.to_dict()