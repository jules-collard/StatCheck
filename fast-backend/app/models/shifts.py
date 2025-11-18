from pydantic import BaseModel


class ShiftBase(BaseModel):
    id: int
    gameID: int
    playerID: int
    teamID: int
    period: int
    durationSec: int
    startTimeSec: int
    endTimeSec: int
    shiftNumber: int


class SplitShiftBase(BaseModel):
    shiftID: int
    split: int
    gameID: int
    playerID: int
    teamID: int
    period: int
    startTimeSec: int
    endTimeSec: int
    duration: int
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


