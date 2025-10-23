from typing import Optional, List

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
    isActive: bool
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

class SkaterTotalsRecords(BaseModel):
    maxGamesPlayed: int = Field(ge=0)
    maxGoals: int = Field(ge=0)
    maxAssists: int = Field(ge=0)
    maxPoints: int = Field(ge=0)
    maxPlusMinus: int
    maxPenaltyMinutes: int = Field(ge=0)
    maxHits: int = Field(ge=0)
    maxShotsOnGoal: int = Field(ge=0)
    maxBlocks: int = Field(ge=0)

class SkaterTotals(BaseModel):
    gamesPlayed: int = Field(ge=0)
    goals: int = Field(ge=0)
    assists: int = Field(ge=0)
    plusMinus: int
    hits: int = Field(ge=0)
    sog: int = Field(ge=0)
    blocks: int = Field(ge=0)
    penaltyMinutes: int = Field(ge=0)
    avgTOI: float = Field(ge=0)
    records: Optional[SkaterTotalsRecords] = Field(default=None)

class SkaterLeaderboardItem(BaseModel):
    playerID: int = Field(gt=0)
    fullName: str
    position: str = Field(pattern=r'^[GDLCR]$')
    isActive: bool
    qualified: bool
    teamTriCodes: list[str] = Field(min_length=1)
    totals: SkaterTotals
    
class SkaterShooting(BaseModel):
    xg: float = Field(ge=0)
    xgGoals: int = Field(ge=0)
    fenwick: int = Field(ge=0)

class SkaterOnIce(BaseModel):
    onIceShootingPct: float = Field(ge=0, le=1)
    fenwickFor: int = Field(ge=0)
    fenwickAgainst: int = Field(ge=0)
    corsiFor: int = Field(ge=0)
    corsiAgainst: int = Field(ge=0)
    xgFor: float = Field(ge=0)
    xgAgainst: float = Field(ge=0)
    oZoneStarts: int = Field(ge=0)
    nZoneStarts: int = Field(ge=0)
    dZoneStarts: int = Field(ge=0)

class SkaterStats(BaseModel):
    playerID: int = Field(gt=0)
    season: int = Field(gt=0)
    teamTriCodes: List[str] = Field(min_length=1)
    totals: SkaterTotals
    shooting: Optional[SkaterShooting] = Field(default=None)
    onIce: Optional[SkaterOnIce] = Field(default=None)

class GoalieTotalsRecords(BaseModel):
    maxGamesPlayed: int = Field(ge=0)
    maxGamesStarted: int = Field(ge=0)
    maxWins: int = Field(ge=0)
    maxLosses: int = Field(ge=0)
    minGAA: float = Field(ge=0)
    maxSavePct: float = Field(ge=0, le=1)

class GoalieTotals(BaseModel):
    gamesPlayed: int = Field(ge=0)
    gamesStarted: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    goalsAgainst: int = Field(ge=0)
    goalsAgainstAvg: float = Field(ge=0)
    savePct: Optional[float] = Field(ge=0, le=1)
    evenStrengthSavePct: Optional[float] = Field(ge=0, le=1)
    powerPlaySavePct: Optional[float] = Field(ge=0, le=1)
    records: Optional[GoalieTotalsRecords] = Field(default=None)

class GoalieAdvanced(BaseModel):
    xgAgainst: float = Field(ge=0)
    xgGoalsAgainst: int = Field(ge=0)
    fenwickAgainst: int = Field(ge=0)

class GoalieLeaderboardItem(BaseModel):
    playerID: int = Field(gt=0)
    fullName: str
    position: str = Field(pattern=r'^G$')
    qualified: bool
    isActive: bool
    teamTriCodes: list[str] = Field(min_length=1)
    totals: GoalieTotals
    advanced: Optional[GoalieAdvanced] = Field(default=None)

class GoalieStats(BaseModel):
    playerID: int = Field(gt=0)
    season: int = Field(gt=0)
    teamTriCodes: List[str] = Field(min_length=1)
    qualified: bool
    totals: GoalieTotals
    advanced: Optional[GoalieAdvanced] = Field(default=None)
