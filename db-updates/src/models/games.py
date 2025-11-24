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