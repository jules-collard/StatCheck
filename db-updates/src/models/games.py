from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel


class GameBase(BaseModel):
    id: int
    season: int
    gameType: int
    neutralSite: bool
    gameDate: date
    gameState: str
    gameScheduleState: str
    defaultVenue: str
    awayTeamID: int
    awayTeamScore: int
    homeTeamID: int
    homeTeamScore: int
    lastPeriodType: str
    metaDateTime: datetime


class EventTypeBase(BaseModel):
    typeCode: int
    typeDescKey: str


class EventBase(BaseModel):
    eventID: int
    gameID: int
    timeInPeriodSec: Optional[int] = None
    awayGoalie: Optional[int] = None
    awaySkaters: Optional[int] = None
    homeGoalie: Optional[int] = None
    homeSkaters: Optional[int] = None
    homeTeamDefendingSide: str
    typeCode: int
    sortOrder: Optional[int] = None
    period: Optional[int] = None
    periodType: Optional[str] = None
    eventOwnerTeamID: Optional[int] = None
    playerID: int
    losingPlayerID: int
    winningPlayerID: int
    xCoord: Optional[float] = None
    yCoord: Optional[float] = None
    zoneCode: Optional[str] = None
    hittingPlayerID: Optional[int] = None
    hitteePlayerID: Optional[int] = None
    blockingPlayerID: Optional[int] = None
    shootingPlayerID: Optional[int] = None
    shotType: Optional[str] = None
    goalieInNetID: Optional[int] = None
    eventOwnerPlayerID: Optional[int] = None
    duration: Optional[int] = None
    committedByPlayerID: Optional[int] = None
    drawnByPlayerID: Optional[int] = None
    scoringPlayerID: Optional[int] = None
    assist1PlayerID: Optional[int] = None
    assist2PlayerID: Optional[int] = None
    xg: Optional[float] = None


class ShiftBase(BaseModel):
    id: int
    durationSec: int
    startTimeSec: int
    endTimeSec: int
    gameID: int
    period: int
    playerID: int
    shiftNumber: int
    teamID: int


class SplitShiftBase(BaseModel):
    shiftID: int
    split: int
    teamID: int
    playerID: int
    gameID: int
    period: int
    startTimeSec: int
    endTimeSec: int
    splitDuration: int
    attackingSkaters: int
    defendingSkaters: int
    attackingGoalie: bool
    defendingGoalie: bool
    goalsFor: int
    goalsAgainst: int
    sogFor: int
    sogAgainst: int
    fenwickFor: int
    fenwickAgainst: int
    corsiFor: int
    corsiAgainst: int
    xgFor: float
    xgAgainst: float
    dZoneStarts: int
    nZoneStarts: int
    oZoneStarts: int


class GoalieAppearanceBase(BaseModel):
    playerID: int
    gameID: int
    teamID: int
    evenStrengthSaves: int
    evenStrengthShotsAgainst: int
    powerPlaySaves: int
    powerPlayShotsAgainst: int
    shorthandedSaves: int
    shorthandedShotsAgainst: int
    saves: int
    shotsAgainst: int
    toiSeconds: int
    starter: bool
    played: bool
    decision: Optional[str] = None


class SkaterAppearanceBase(BaseModel):
    appearanceID: int
    playerID: int
    teamID: int
    gameID: int
    position: str
    goals: int
    powerPlayGoals: int
    assists: int
    plusMinus: int
    pim: int
    hits: int
    sog: int
    blocks: int
    giveaways: int
    takeaways: int
    toiSeconds: int