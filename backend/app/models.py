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
    

class GameType(db.Model):
    __tablename__ = "game_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column()


class Game(db.Model):
    __tablename__ = "games"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    season: so.Mapped[int] = so.mapped_column()
    gameType: so.Mapped[int] = so.mapped_column(sa.ForeignKey(GameType.typeCode))
    inHHOF: so.Mapped[int] = so.mapped_column(nullable=True)
    startTimeUTC: so.Mapped[datetime] = so.mapped_column()
    venueUTCOffset: so.Mapped[int] = so.mapped_column()
    gameState: so.Mapped[str] = so.mapped_column()
    gameScheduleState: so.Mapped[str] = so.mapped_column()
    defaultVenue: so.Mapped[str] = so.mapped_column()
    awayTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    awayTeamScore: so.Mapped[int] = so.mapped_column()
    homeTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    homeTeamScore: so.Mapped[int] = so.mapped_column()
    maxRegulationPeriod: so.Mapped[int] = so.mapped_column()
    lastPeriodType: so.Mapped[str] = so.mapped_column()
    winningGoalieID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    winningGoalscorerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.awayTeamID} at {self.homeTeamID} {self.startTimeUTC}>"