from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class TeamBase(BaseModel):
    id: int
    franchiseID: Optional[int] = None
    fullName: str
    triCode: str
    placeName: Optional[str] = None
    commonNameFR: Optional[str] = None
    fullNameFR: Optional[str] = None
    metaDateTime: datetime