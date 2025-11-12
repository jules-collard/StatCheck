from typing import Optional, List

from pydantic import BaseModel

from .teams import TeamBase

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
    birthDate: str
    birthCountry: str
    shootsCatches: str
    draftYear: Optional[int] = None
    draftTeamAbbrev: Optional[str] = None
    draftRound: Optional[int] = None
    draftPickInRound: Optional[int] = None
    draftOverallPick: Optional[int] = None
    inHHOF: Optional[bool] = False

    awards: Optional[List['AwardBase']] = []

class PlayerRead(BaseModel):
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
    birthDate: str
    birthCountry: str
    shootsCatches: str
    draftYear: Optional[int] = None
    draftTeamAbbrev: Optional[str] = None
    draftRound: Optional[int] = None
    draftPickInRound: Optional[int] = None
    draftOverallPick: Optional[int] = None
    inHHOF: Optional[bool] = False

    awards: Optional[List['AwardBase']] = []
    team: Optional['TeamBase'] = None


class PlayerUpdate(BaseModel):
    id: int
    isActive: Optional[bool]
    currentTeamID: Optional[int]
    sweaterNumber: Optional[int]
    position: Optional[str]
    headshot: Optional[str]
    heightInInches: Optional[int]
    heightInCentimeters: Optional[int]
    weightInPounds: Optional[int]
    weightInKilograms: Optional[int]
    inHHOF: Optional[bool]
    awards: Optional[List['AwardBase']]


class PlayerListItem(BaseModel):
    id: int
    fullName: str
    isActive: bool
    position: str
    teamTriCode: Optional[str]
    headshot: Optional[str]


class AwardBase(BaseModel):
    awardName: str
    season: int
    winningPlayerID: int
    