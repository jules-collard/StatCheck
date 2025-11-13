from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.games import GameBase
from app.db.database import get_session
from app.services.game_service import GameService

router = APIRouter(prefix='/api/games')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_game(
    game: GameBase,
    session: AsyncSession = Depends(get_session)
):
    service = GameService(session)
    if await service.game_exists(game.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Game already exists')
    return service.add_game(game)