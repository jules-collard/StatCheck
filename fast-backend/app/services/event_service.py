from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from app.models.events import EventTypeBase
from app.db.schema import EventType

class EventService:

    def __init__(self, session: AsyncSession):
        self.session = session

    def add_event_types(self, event_types: List[EventTypeBase]):
        try:
            event_type_objs = [EventType(**event_type.model_dump()) for event_type in event_types]
            self.session.add_all(event_type_objs)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.json())