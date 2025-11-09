from typing import Optional, List
from datetime import datetime, date

from pydantic import BaseModel, Field

class PlayerBase(BaseModel):
    id: int
    isActive: bool
    currentTeamID: Optional[int] = None
    firstName: str
    lastName: str
    sweaterNumber: Optional[int] = None
    position: str
    headshot: Optional[str] = None
    heightInInches: Optional[int] = None
    heightInCentimeters: Optional[int] = None
    weightInPounds: Optional[int] = None
    weightInKilograms: Optional[int] = None
    birthDate: date
    birthCountry: str
    shootsCatches: str
    draftYear: Optional[int] = None
    draftTeamAbbrev: Optional[str] = None
    draftRound: Optional[int] = None
    draftPickInRound: Optional[int] = None
    draftOverallPick: Optional[int] = None
    inHHOF: Optional[bool] = False
    metaDateTime: datetime = Field(default_factory=datetime.now)

    awards: Optional[List['AwardBase']] = []


class AwardBase(BaseModel):
    awardName: str
    season: int
    winningPlayerID: int