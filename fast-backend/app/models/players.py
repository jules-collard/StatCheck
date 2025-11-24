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


class SkaterStats(BaseModel):
    playerID: int
    season: int
    teamTriCodes: List[str]
    qualified: bool
    shotsQualified: bool
    totals: 'SkaterTotals'
    shooting: Optional['SkaterShooting'] = None
    onice: Optional['SkaterOnIce'] = None


class SkaterTotals(BaseModel):
    gamesPlayed: int
    goals: int
    assists: int
    plusMinus: int
    penaltyMinutes: int
    hits: int
    sog: int
    blocks: int
    avgTOI: float


class SkaterShooting(BaseModel):
    xg: Optional[float]
    xgGoals: Optional[int]
    fenwick: Optional[int]


class SkaterOnIce(BaseModel):
    onIceShootingPct: Optional[float]
    fenwickFor: Optional[int]
    fenwickAgainst: Optional[int]
    corsiFor: Optional[int]
    corsiAgainst: Optional[int]
    xgFor: Optional[float]
    xgAgainst: Optional[float]
    oZoneStarts: Optional[int]
    nZoneStarts: Optional[int]
    dZoneStarts: Optional[int]


class SkaterLeaderboardItem(BaseModel):
    playerID: int
    fullName: str
    position: str
    isActive: bool
    qualified: bool
    shotsQualified: bool
    teamTriCodes: list[str]
    totals: SkaterTotals
    shooting: SkaterShooting
    onIce: SkaterOnIce


class GoalieStats(BaseModel):
    playerID: int
    season: int
    teamTriCodes: List[str]
    qualified: bool
    totals: 'GoalieTotals'
    advanced: Optional['GoalieAdvanced']


class GoalieTotals(BaseModel):
    gamesPlayed: int
    gamesStarted: int
    wins: int
    losses: int
    goalsAgainst: int
    goalsAgainstAvg: float
    savePct: Optional[float]
    evenStrengthSavePct: Optional[float]
    powerPlaySavePct: Optional[float]


class GoalieAdvanced(BaseModel):
    xgAgainst: Optional[float]
    xgGoalsAgainst: Optional[int]
    fenwickAgainst: Optional[int]


class GoalieLeaderboardItem(BaseModel):
    playerID: int
    fullName: str
    position: str
    qualified: bool
    isActive: bool
    teamTriCodes: list[str]
    totals: GoalieTotals
    advanced: Optional[GoalieAdvanced]