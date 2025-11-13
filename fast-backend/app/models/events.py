from typing import Optional, Literal

from pydantic import BaseModel


class EventTypeBase(BaseModel):
    typeCode: int
    typeDescKey: str


class EventBase(BaseModel):
    eventID: int
    gameID: int
    timeInPeriodSec: Optional[int]
    awayScore: Optional[int]
    homeScore: Optional[int]
    awayGoalie: Optional[int]
    awaySkaters: Optional[int]
    homeGoalie: Optional[int]
    homeSkaters: Optional[int]
    homeTeamDefendingSide: Optional[Literal['left', 'right']]
    typeCode: int
    sortOrder: Optional[int]
    period: Optional[int]
    periodType: Optional[str]
    eventOwnerTeamID: Optional[int]
    playerID: int
    losingPlayerID: int
    winningPlayerID: int
    xCoord: Optional[float]
    yCoord: Optional[float]
    xStd: Optional[float]
    yStd: Optional[float]
    zoneCode: Optional[str]
    hittingPlayerID: Optional[int]
    hitteePlayerID: Optional[int]
    blockingPlayerID: Optional[int]
    shootingPlayerID: Optional[int]
    shotType: Optional[str]
    goalieInNetID: Optional[int]
    eventOwnerPlayerID: Optional[int]
    duration: Optional[int]
    committedByPlayerID: Optional[int]
    drawnByPlayerID: Optional[int]
    scoringPlayerID: Optional[int]
    assist1PlayerID: Optional[int]
    assist2PlayerID: Optional[int]
    xg: Optional[float]