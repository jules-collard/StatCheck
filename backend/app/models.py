from datetime import datetime, timezone, date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
import inspect

class Team(db.Model):
    __tablename__ = 'teams'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fullName: so.Mapped[str] = so.mapped_column()
    commonName: so.Mapped[str] = so.mapped_column()
    placeName: so.Mapped[str] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.fullName}>"
    
    def to_dict(self):
        return {
            'id':self.id,
            'fullName': self.fullName
        }
    
    def from_dict(self, data):
        # Isolate class attributes
        attrs = [i[0] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]))]
        for field in attrs:
            if field in data:
                setattr(self, field, data[field])
    

class Player(db.Model):
    __tablename__ = 'players'
                     
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    isActive: so.Mapped[int] = so.mapped_column(sa.CheckConstraint('''isActive IN (0,1)'''))
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
    inHHOF: so.Mapped[int] = so.mapped_column(sa.CheckConstraint('''inHHOF IN (0,1)'''), nullable=True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.firstName} {self.lastName}>"
    
    def to_dict(self):
        return {
            'id':self.id,
            'name': f"{self.firstName} {self.lastName}"
        }
    
    def from_dict(self, data):
        # Isolate class attributes
        attrs = [i[0] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]))]
        for field in attrs:
            if field in data:
                setattr(self, field, data[field])
    

class GameType(db.Model):
    __tablename__ = "game_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''typeDescKey IN ("REG", "POST")'''))


class Game(db.Model):
    __tablename__ = "games"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    season: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("season > 0"))
    gameType: so.Mapped[int] = so.mapped_column(sa.ForeignKey(GameType.typeCode))
    neutralSite: so.Mapped[int] = so.mapped_column(sa.CheckConstraint('''neutralSite IN (0,1)'''), nullable=True)
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
    winningGoalieID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    winningGoalscorerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.awayTeamID} at {self.homeTeamID} {self.startTimeUTC}>"
    

class EventType(db.Model):
    __tablename__ = "event_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column()


class Event(db.Model):
    __tablename__ = "events"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timeInPeriodMin: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("timeInPeriodMin >= 0 AND timeInPeriodMin <= 20"))
    timeInPeriodSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("timeInPeriodSec >= 0 AND timeInPeriodSec <= 60"))
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
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id))
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Event: {self.typeCode}>"