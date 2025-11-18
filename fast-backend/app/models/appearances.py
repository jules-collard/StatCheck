from typing import Optional, Literal

from pydantic import BaseModel


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
    decision: Optional[Literal['W', 'L', 'O']] = None


class SkaterAppearanceBase(BaseModel):
    playerID: int
    teamID: int
    gameID: int
    position: Literal['D','L','R','C']
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