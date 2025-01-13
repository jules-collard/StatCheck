from datetime import datetime, timezone, date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Team(db.Model):
    __tablename__ = 'teams'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fullName: so.Mapped[str] = so.mapped_column()
    commonName: so.Mapped[str] = so.mapped_column()
    placeName: so.Mapped[str] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.fullName}>"
    

class Player(db.Model):
    __tablename__ = 'players'
    
    """ NOT WORKING
    __tableargs__ = (sa.CheckConstraint('''isActive IN (0,1)'''),
                     sa.CheckConstraint("sweaterNumber >= 0"),
                     sa.CheckConstraint("heightInInches >= 0"),
                     sa.CheckConstraint("heightInCentimeters >= 0"),
                     sa.CheckConstraint("weightInPounds >= 0"),
                     sa.CheckConstraint("weightInKilograms >= 0"),
                     sa.CheckConstraint('''shootsCatches IN ("L","R")'''),
                     sa.CheckConstraint('''isActive IN (0,1)'''))
    """
                     
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    isActive: so.Mapped[int] = so.mapped_column()
    currentTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    firstName: so.Mapped[str] = so.mapped_column()
    lastName: so.Mapped[str] = so.mapped_column()
    sweaterNumber: so.Mapped[int] = so.mapped_column(nullable=True)
    position: so.Mapped[str] = so.mapped_column()
    headshot: so.Mapped[str] = so.mapped_column()
    heroImage: so.Mapped[str] = so.mapped_column()
    heightInInches: so.Mapped[int] = so.mapped_column(nullable=True)
    heightInCentimeters: so.Mapped[int] = so.mapped_column(nullable=True)
    weightInPounds: so.Mapped[int] = so.mapped_column(nullable=True)
    weightInKilograms: so.Mapped[int] = so.mapped_column(nullable=True)
    birthDate: so.Mapped[date] = so.mapped_column()
    birthCity: so.Mapped[str] = so.mapped_column(nullable=True)
    birthCountry: so.Mapped[str] = so.mapped_column(nullable=True)
    shootsCatches: so.Mapped[str] = so.mapped_column()
    draftYear: so.Mapped[int] = so.mapped_column(nullable=True)
    draftTeamAbbrev: so.Mapped[str] = so.mapped_column(nullable=True)
    draftRound: so.Mapped[int] = so.mapped_column(nullable=True)
    draftPickInRound: so.Mapped[int] = so.mapped_column(nullable=True)
    draftOverallPick: so.Mapped[str] = so.mapped_column(nullable=True)
    inHHOF: so.Mapped[int] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.firstName} {self.lastName}>"
    
    def to_dict(self):
        return {
            'id':self.id,
            'name': f"{self.firstName} {self.lastName}"
        }
    

class GameType(db.Model):
    __tablename__ = "game_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column()


class Game(db.Model):
    __tablename__ = "games"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    season: so.Mapped[int] = so.mapped_column()
    gameType: so.Mapped[int] = so.mapped_column(sa.ForeignKey(GameType.typeCode))
    neutralSite: so.Mapped[int] = so.mapped_column(nullable=True)
    startTimeUTC: so.Mapped[datetime] = so.mapped_column()
    venueUTCOffset: so.Mapped[int] = so.mapped_column()
    gameState: so.Mapped[str] = so.mapped_column()
    gameScheduleState: so.Mapped[str] = so.mapped_column()
    defaultVenue: so.Mapped[str] = so.mapped_column()
    awayTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    awayTeamScore: so.Mapped[int] = so.mapped_column()
    homeTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    homeTeamScore: so.Mapped[int] = so.mapped_column()
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
    timeInPeriod: so.Mapped[str] = so.mapped_column()
    timeRemaining: so.Mapped[str] = so.mapped_column()
    awayGoalie: so.Mapped[int] = so.mapped_column()
    awaySkaters: so.Mapped[int] = so.mapped_column()
    homeGoalie: so.Mapped[int] = so.mapped_column()
    homeSkaters: so.Mapped[int] = so.mapped_column()
    homeTeamDefendingSide: so.Mapped[str] = so.mapped_column()
    typeCode: so.Mapped[int] = so.mapped_column(sa.ForeignKey(EventType.typeCode))
    sortOrder: so.Mapped[int] = so.mapped_column()
    period: so.Mapped[int] = so.mapped_column()
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
    penaltyDuration: so.Mapped[str] = so.mapped_column(nullable=True)
    committedByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    drawnByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    scoringPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    assist1PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    assist2PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id))
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Event: {self.typeCode}>"