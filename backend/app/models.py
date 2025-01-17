from datetime import datetime, timezone, date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
import inspect

class Util():
    def from_dict(self, data):
        # Isolate class attributes
        attrs = [i[0] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]))]
        
        for field in attrs:
            if field in data:
                setattr(self, field, data[field])


class Team(db.Model, Util):
    __tablename__ = 'teams'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    franchiseID: so.Mapped[int] = so.mapped_column(nullable=True)
    fullName: so.Mapped[str] = so.mapped_column()
    triCode: so.Mapped[str] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    players: so.WriteOnlyMapped['Player'] = so.relationship(back_populates='team')

    def __repr__(self):
        return f"Team: <{self.fullName}>"
    
    def to_dict(self):
        return {
            'id':self.id,
            'fullName': self.fullName
        }
    

class Player(db.Model, Util):
    __tablename__ = 'players'
                     
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    isActive: so.Mapped[bool] = so.mapped_column()
    currentTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    firstName: so.Mapped[str] = so.mapped_column()
    lastName: so.Mapped[str] = so.mapped_column()
    sweaterNumber: so.Mapped[int] = so.mapped_column(nullable=True)
    position: so.Mapped[str] = so.mapped_column()
    headshot: so.Mapped[str] = so.mapped_column(nullable=True)
    heroImage: so.Mapped[str] = so.mapped_column(nullable=True)
    heightInInches: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("heightInInches >= 0"), nullable=True)
    heightInCentimeters: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("heightInCentimeters >= 0"), nullable=True)
    weightInPounds: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("weightInPounds >= 0"), nullable=True)
    weightInKilograms: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("weightInKilograms >= 0"), nullable=True)
    birthDate: so.Mapped[date] = so.mapped_column()
    birthCity: so.Mapped[str] = so.mapped_column(nullable=True)
    birthCountry: so.Mapped[str] = so.mapped_column(nullable=True)
    shootsCatches: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''shootsCatches IN ("L","R")'''))
    draftYear: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftYear > 0"), nullable=True)
    draftTeamAbbrev: so.Mapped[str] = so.mapped_column(nullable=True)
    draftRound: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftRound > 0"), nullable=True)
    draftPickInRound: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftPickInRound > 0"), nullable=True)
    draftOverallPick: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftOverallPick > 0"), nullable=True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    team: so.Mapped[Team] = so.relationship(back_populates='players')

    def __repr__(self):
        return f"Player: <{self.firstName} {self.lastName}>"
    
    def to_dict(self):
        attrs_dict = {i[0]:i[1] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]) and not i[0] == 'metaDateTime')}
        return attrs_dict
    

class GameType(db.Model):
    __tablename__ = "game_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''typeDescKey IN ("REG", "POST")'''))

    def from_dict(self, data):
        attrs = ["typeCode", "typeDescKey"]
        for field in attrs:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f"GameType: <{self.typeCode}:{self.typeDescKey}>"

class Game(db.Model, Util):
    __tablename__ = "games"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    season: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("season > 0"))
    gameType: so.Mapped[int] = so.mapped_column(sa.ForeignKey(GameType.typeCode))
    neutralSite: so.Mapped[bool] = so.mapped_column()
    startTimeUTC: so.Mapped[datetime] = so.mapped_column()
    venueUTCOffset: so.Mapped[int] = so.mapped_column()
    gameState: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''gameState = "OFF"'''))
    gameScheduleState: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''gameScheduleState = "OK"'''))
    defaultVenue: so.Mapped[str] = so.mapped_column()
    awayTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    awayTeamScore: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("awayTeamScore >= 0"))
    homeTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    homeTeamScore: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("homeTeamScore >= 0"))
    maxRegulationPeriods: so.Mapped[int] = so.mapped_column()
    lastPeriodType: so.Mapped[str] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"Game: <{self.awayTeamID} at {self.homeTeamID} {self.startTimeUTC}>"
    

class EventType(db.Model, Util):
    __tablename__ = "event_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column()

    def from_tuple(self, tup):
        self.typeCode = tup[0]
        self.typeDescKey = tup[1]

    def __repr__(self):
        return f"EventType: <{self.typeCode}:{self.typeDescKey}>"


class Event(db.Model, Util):
    __tablename__ = "events"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timeInPeriodSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("timeInPeriodSec >= 0"))
    awayGoalie: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("awayGoalie IN (0,1)"))
    awaySkaters: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("awaySkaters >= 0"))
    homeGoalie: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("homeGoalie IN (0,1)"))
    homeSkaters: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("homeSkaters >= 0"))
    homeTeamDefendingSide: so.Mapped[str] = so.mapped_column()
    typeCode: so.Mapped[int] = so.mapped_column(sa.ForeignKey(EventType.typeCode))
    sortOrder: so.Mapped[int] = so.mapped_column()
    period: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("period > 0"))
    periodType: so.Mapped[str] = so.mapped_column()
    eventOwnerTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), nullable=True)
    losingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    winningPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    xCoord: so.Mapped[float] = so.mapped_column(nullable=True)
    yCoord: so.Mapped[float] = so.mapped_column(nullable=True)
    zoneCode: so.Mapped[str] = so.mapped_column(nullable=True)
    hittingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    hitteePlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    blockingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    shootingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    reason: so.Mapped[str] = so.mapped_column(nullable=True)
    shotType: so.Mapped[str] = so.mapped_column(nullable=True)
    goalieInNetID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    eventOwnerPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    penaltyDuration: so.Mapped[int] = so.mapped_column(nullable=True)
    committedByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    drawnByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    scoringPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    assist1PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    assist2PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), primary_key=True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Event: {self.typeCode}>"
    

class Shift(db.Model, Util):
    __tablename__ = "shifts"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    durationSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("durationSec >= 0"))
    startTimeSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("startTimeSec >= 0"))
    endTimeSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("endTimeSec >= 0"))
    eventNumber: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("eventNumber >= 0"))
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id))
    period: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("period > 0"))
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    shiftNumber: so.Mapped[int] = so.mapped_column()
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))


class PlayerGame(db.Model, Util):
    __tablename__ = "player_games"

    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), primary_key=True)
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), primary_key=True)
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), primary_key=True)

    def __repr__(self):
        return f"Player {self.playerID} - Team {self.teamID} - Game {self.gameID}"
