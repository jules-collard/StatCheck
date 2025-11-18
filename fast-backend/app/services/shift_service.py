from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert

from app.db.schema import Shift
from app.models.shifts import ShiftBase

class ShiftService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_shifts_exist(self, gameID: int):
        stmt = select(Shift).where(Shift.gameID == gameID)
        shifts = await self.session.scalars(stmt)
        if len(shifts.all() > 0):
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Shifts already in database (Game {gameID})")
        
    async def insert_shifts(self, gameID: int, shifts: List[ShiftBase]):
        self.check_shifts_exist(gameID)
        try:
            stmt = insert(Shift).values([shift.model_dump() for shift in shifts])
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))