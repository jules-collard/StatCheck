from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from app.models.events import EventTypeBase, EventBase, EventPatchXG
from app.db.schema import EventType, Event, Game

class EventService:

    def __init__(self, session: AsyncSession):
        self.session = session

    def add_event_types(self, event_types: List[EventTypeBase]):
        try:
            event_type_objs = [EventType(**event_type.model_dump()) for event_type in event_types]
            self.session.add_all(event_type_objs)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def check_events_exist(self, gameID):
        stmt = select(Event).where(Event.gameID == gameID)
        events = await self.session.scalars(stmt)
        if len(events.all()) > 0:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='Events already in database')
        
    async def insert_events(self, gameID: int, events: List[EventBase]):
        await self.check_events_exist(gameID)
        try:
            stmt = insert(Event).values([event.model_dump() for event in events])
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
        
    async def get_events(self, gameID: int):
        events: List[Event] = await self.session.scalars(select(Event).where(Event.gameID == gameID))
        try:
            event_dicts = [event.to_read().model_dump() for event in events]
            return event_dicts
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def get_events_shift(self, gameID: int, period: int, startTimeSec: int, endTimeSec: int):
        stmt = (select(Event.period, Event.timeInPeriodSec, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.typeCode, Event.homeScore, Event.awayScore, Event.xStd, Event.eventOwnerTeamID, Game.homeTeamID, Event.xg)
                .join(Event.game)
                .where(Event.gameID == gameID,
                    Event.period == period,
                    Event.timeInPeriodSec >= startTimeSec,
                    Event.timeInPeriodSec <= endTimeSec)
                .order_by(Event.timeInPeriodSec, Event.sortOrder))
        result = await self.session.execute(stmt)
        return [row._asdict() for row in result.all()]
        
    async def update_xg(self, shots: List[EventPatchXG]):
        shot_dicts = [shot.model_dump() for shot in shots]
        await self.session.execute(update(Event), shot_dicts)