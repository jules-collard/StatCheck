from typing import Optional

from pydantic import BaseModel

class TeamBase(BaseModel):
    id: int
    franchiseID: Optional[int] = None
    fullName: str
    triCode: str
    placeName: Optional[str]

class TeamRead(BaseModel):
    id: int
    franchiseID: Optional[int] = None
    fullName: str
    triCode: str