from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam
from pydantic import ValidationError

from app.models.events import EventTypeBase, EventBase, EventPatchXG
from app.db.schema import EventType, Event

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
            eventObjs = [Event(**event.model_dump()) for event in events]
            self.session.add_all(eventObjs)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def get_events(self, gameID: int):
        events: List[Event] = await self.session.scalars(select(Event).where(Event.gameID == gameID))
        try:
            event_dicts = [event.to_read().model_dump() for event in events]
            return event_dicts
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())
        
    async def update_xg(self, shots: List[EventPatchXG]):
        shot_dicts = [shot.model_dump() for shot in shots]
        await self.session.execute(update(Event), shot_dicts)