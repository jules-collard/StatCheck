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
    currentTeamID: Optional[int] = Field(default=None)
    firstName: str
    lastName: str
    sweaterNumber: Optional[int] = Field(default=None)
    position: str = Field(pattern=r'^[GDLCR]$')
    headshot: str = Field(pattern=r'^.*\.png$')
    heightInInches: int = Field(gt=0)
    heightInCentimeters: int = Field(gt=0)
    weightInPounds: int = Field(gt=0)
    weightInKilograms: int = Field(gt=0)
    birthDate: str
    birthCountry: str
    shootsCatches: str = Field(pattern=r'^[LR]$')
    draftYear: Optional[int] = Field(default=None)
    draftTeamAbbrev: Optional[str] = Field(default=None)
    draftRound: Optional[int] = Field(default=None)
    draftPickInRound: Optional[int] = Field(default=None)
    draftOverallPick: Optional[int] = Field(default=None)
    inHHOF: Optional[bool] = Field(default=False)
    team: Optional[TeamInfo] = Field(default=None)
    awards: list[AwardInfo]

class SkaterTotals(BaseModel):
    gamesPlayed: int = Field(ge=0)
    goals: int = Field(ge=0)
    assists: int = Field(ge=0)
    powerPlayGoals: int = Field(ge=0)
    plusMinus: int
    hits: int = Field(ge=0)
    sog: int = Field(ge=0)
    blocks: int = Field(ge=0)
    penaltyMinutes: int = Field(ge=0)
    avgTOI: float = Field(ge=0)

class SkaterShooting(BaseModel):
    xg: float = Field(ge=0)
    xgGoals: int = Field(ge=0)
    fenwick: int = Field(ge=0)

class SkaterStats(BaseModel):
    playerID: int = Field(gt=0)
    season: int = Field(gt=0)
    teamTriCode: str = Field(pattern=r'^[A-Z]{3}$')
    totals: SkaterTotals
    shooting: Optional[SkaterShooting] = Field(default=None)

class GoalieTotals(BaseModel):
    gamesPlayed: int = Field(ge=0)
    gamesStarted: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    goalsAgainst: int = Field(ge=0)
    goalsAgainstAvg: float = Field(ge=0)
    savePct: float = Field(ge=0, le=1)
    evenStrengthSavePct: float = Field(ge=0, le=1)
    powerPlaySavePct: float = Field(ge=0, le=1)

class GoalieAdvanced(BaseModel):
    xgAgainst: float = Field(ge=0)
    xgGoalsAgainst: int = Field(ge=0)
    fenwickAgainst: int = Field(ge=0)

class GoalieStats(BaseModel):
    playerID: int = Field(gt=0)
    season: int = Field(gt=0)
    teamTriCode: str = Field(pattern=r'^[A-Z]{3}$')
    totals: GoalieTotals
    advanced: Optional[GoalieAdvanced] = Field(default=None)