from typing import Optional, Literal

from pydantic import BaseModel


class EventTypeBase(BaseModel):
    typeCode: int
    typeDescKey: str


class EventBase(BaseModel):
    eventID: int
    gameID: int
    timeInPeriodSec: int
    awayScore: Optional[int] = 0
    homeScore: Optional[int] = 0
    awayGoalie: Optional[int] = None
    awaySkaters: Optional[int] = None
    homeGoalie: Optional[int] = None
    homeSkaters: Optional[int] = None
    homeTeamDefendingSide: Optional[Literal['left', 'right']] = None
    typeCode: int
    sortOrder: Optional[int] = None
    period: int
    periodType: Optional[str] = None
    eventOwnerTeamID: Optional[int] = None
    losingPlayerID: Optional[int] = None
    winningPlayerID: Optional[int] = None
    xCoord: Optional[float] = None
    yCoord: Optional[float] = None
    xStd: Optional[float] = None
    yStd: Optional[float] = None
    zoneCode: Optional[Literal['D', 'N', 'O']] = None
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
    highlightClipSharingURL: Optional[str] = None

class EventRead(BaseModel):
    eventID: int
    gameID: int
    timeInPeriodSec: int
    awayGoalie: Optional[int] = None
    awaySkaters: Optional[int] = None
    homeGoalie: Optional[int] = None
    homeSkaters: Optional[int] = None
    homeTeamDefendingSide: Optional[Literal['left', 'right']] = None
    typeCode: int
    sortOrder: Optional[int] = None
    period: int
    periodType: Optional[str] = None
    eventOwnerTeamID: Optional[int] = None
    shootingPlayerID: Optional[int] = None
    xCoord: Optional[float] = None
    yCoord: Optional[float] = None
    xStd: Optional[float] = None
    yStd: Optional[float] = None
    zoneCode: Optional[Literal['D', 'N', 'O']] = None
    shotType: Optional[str] = None
    goalieInNetID: Optional[int] = None


class EventReadShift(BaseModel):
    period: int
    timeInPeriodSec: int
    awayGoalie: Optional[int]
    awaySkaters: Optional[int]
    homeGoalie: Optional[int]
    homeSkaters: Optional[int]
    typeCode: int
    xStd: Optional[int]
    homeScore: int
    awayScore: int
    eventOwnerTeamID: Optional[int]
    homeTeamID: int
    xg: Optional[float]
    

class EventPatchXG(BaseModel):
    eventID: int
    gameID: int
    xg: float