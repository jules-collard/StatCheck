from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert
from pydantic import ValidationError

from app.db.schema import Shift, SplitShift
from app.models.shifts import ShiftBase, SplitShiftBase

class ShiftService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_shifts_exist(self, gameID: int):
        stmt = select(Shift).where(Shift.gameID == gameID)
        shifts = await self.session.scalars(stmt)
        if len(shifts.all()) > 0:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Shifts already in database (Game {gameID})")
        
    async def check_split_shifts_exist(self, gameID: int):
        stmt = select(SplitShift).where(SplitShift.gameID == gameID)
        splitshifts = await self.session.scalars(stmt)
        if len(splitshifts.all()) > 0:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Split-Shifts already in database (Game {gameID})")
        
    async def insert_shifts(self, gameID: int, shifts: List[ShiftBase]):
        await self.check_shifts_exist(gameID)
        try:
            stmt = insert(Shift).values([shift.model_dump() for shift in shifts])
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
        
    async def get_shifts(self, gameID: int):
        events: List[Shift] = await self.session.scalars(select(Shift).where(Shift.gameID == gameID))
        try:
            shift_dicts = [shift.to_read().model_dump() for shift in events]
            return shift_dicts
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def insert_split_shifts(self, gameID: int, splitshifts: List[SplitShiftBase]):
        await self.check_split_shifts_exist(gameID)
        try:
            stmt = insert(SplitShift).values([splitshift.model_dump() for splitshift in splitshifts])
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))