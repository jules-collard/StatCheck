from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class TeamInfo(BaseModel):
    id: int = Field(gt=0)
    franchiseID: int = Field(gt=0)
    fullName: str
    triCode: str = Field(pattern=r'^[A-Z]{3}$')

class AwardInfo(BaseModel):
    awardName: str
    season: int = Field(gt=0)

class PlayerListItem(BaseModel):
    id: int = Field(gt=0)
    fullName: str
    position: str = Field(pattern=r'^[GDLCR]$')
    teamTriCode: Optional[str] = Field(pattern=r'^[A-Z]{3}$')
    headshot: str = Field(pattern=r'^.*\.png$')

class PlayerInfo(BaseModel):
    id: int = Field(gt=0)
    isActive: bool
    currentTeamID: Optional[int]
    firstName: str
    lastName: str
    sweaterNumber: Optional[int]
    position: str = Field(pattern=r'^[GDLCR]$')
    headshot: str = Field(pattern=r'^.*\.png$')
    heightInInches: int = Field(gt=0)
    heightInCentimeters: int = Field(gt=0)
    weightInPounds: int = Field(gt=0)
    weightInKilograms: int = Field(gt=0)
    birthDate: str
    birthCountry: str
    shootsCatches: str = Field(pattern=r'^[LR]$')
    draftYear: Optional[int]
    draftPickInRound: Optional[int]
    inHHOF: Optional[bool]
    team: Optional[TeamInfo]
    awards: list[AwardInfo]