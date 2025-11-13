from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from app.db.schema import Game
from app.models.games import GameBase

class GameService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def game_exists(self, id: int):
        return await self.session.get(Game, id) is not None
    
    def return_game(self, game: Game):
        try:
            gameObj: GameBase = game.to_read()
            return gameObj.model_dump()
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def get_game(self, id: int):
        game: Game | None = await self.session.get(Game, id)
        if game is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'Game not found')
        else:
            return self.return_game(game)

    def add_game(self, game: GameBase):
        data = game.model_dump()
        data['gameDate'] = datetime.strptime(data.get('gameDate', ''), '%Y-%m-%d').date()
        gameObj = Game(**data)
        self.session.add(gameObj)
        return self.return_game(gameObj)
    
    async def delete_game(self, id: int):
        game: Game | None = await self.session.get(Game, id)
        if game is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
        else:
            await self.session.delete(game)
