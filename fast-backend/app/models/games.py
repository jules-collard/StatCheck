from typing import Literal, Optional

from pydantic import BaseModel

class GameBase(BaseModel):
    id: int
    season: int
    gameType: int
    neutralSite: bool
    gameDate: str
    defaultVenue: str
    awayTeamID: int
    awayTeamScore: int
    homeTeamID: int
    homeTeamScore: int
    lastPeriodType: str

class ScoreTeam(BaseModel):
    id: int
    abbrev: str
    record: Optional[str] = None
    score: Optional[int] = None
    sog: Optional[int] = None

class Clock(BaseModel):
    timeRemaining: str
    inIntermission: bool

class PeriodDescriptor(BaseModel):
    number: int
    periodType: Literal['REG', 'OT', 'SO']

class GameOutcome(BaseModel):
    lastPeriodType: Literal['REG', 'OT', 'SO']

class GameDetails(BaseModel):
    id: int
    startTimeEastern: str
    gameState: Literal['FUT', 'OFF', 'PRE', 'LIVE']
    awayTeam: ScoreTeam
    homeTeam: ScoreTeam
    clock: Optional[Clock] = None
    periodDescriptor: Optional[PeriodDescriptor] = None
    gameOutcome: Optional[GameOutcome] = None

class GameList(BaseModel):
    games: list[GameDetails]

class TeamStandingsItem(BaseModel):
    conferenceAbbrev: Literal['E', 'W']
    divisionAbbrev: Literal['C', 'P', 'M', 'A']
    gamesPlayed: int
    goalDifferential: int
    goalAgainst: int
    goalFor: int
    losses: int
    otLosses: int
    wins: int
    points: int
    pointPctg: float
    leagueSequence: int
    teamAbbrev: str
    teamLogo: str
    l10Wins: int
    l10Losses: int
    l10OtLosses: int