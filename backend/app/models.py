from datetime import datetime, timezone, date
import inspect

import sqlalchemy as sa
import sqlalchemy.orm as so
from pydantic import ValidationError

from app import db
from app.api.api_models import PlayerListItem

class Util():
    def from_dict(self, data):
        # Isolate class attributes
        attrs = [i[0] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]))]
        
        for field in attrs:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        attrs = [i[0] for i in inspect.getmembers(self) if (not i[0].startswith('_') and not inspect.ismethod(i[1]))]
        return {field: getattr(self, field) for field in attrs}


class Team(db.Model, Util):
    __tablename__ = 'teams'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    franchiseID: so.Mapped[int] = so.mapped_column(nullable=True)
    fullName: so.Mapped[str] = so.mapped_column()
    triCode: so.Mapped[str] = so.mapped_column()
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    players: so.Mapped[list['Player']] = so.relationship(back_populates='team')
    homeGames: so.Mapped[list['Game']] = so.relationship(back_populates='homeTeam', foreign_keys='Game.homeTeamID')
    awayGames: so.Mapped[list['Game']] = so.relationship(back_populates='awayTeam', foreign_keys='Game.awayTeamID')

    def __repr__(self):
        return f"Team: <{self.fullName}> ({self.id})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'franchiseID': self.franchiseID,
            'fullName': self.fullName,
            'triCode': self.triCode
        }
    

class Player(db.Model, Util):
    __tablename__ = 'players'
                     
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    isActive: so.Mapped[bool] = so.mapped_column()
    currentTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), nullable=True)
    firstName: so.Mapped[str] = so.mapped_column()
    lastName: so.Mapped[str] = so.mapped_column()
    sweaterNumber: so.Mapped[int] = so.mapped_column(nullable=True)
    position: so.Mapped[str] = so.mapped_column()
    headshot: so.Mapped[str] = so.mapped_column()
    heroImage: so.Mapped[str] = so.mapped_column(nullable=True)
    heightInInches: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("heightInInches >= 0"))
    heightInCentimeters: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("heightInCentimeters >= 0"))
    weightInPounds: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("weightInPounds >= 0"))
    weightInKilograms: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("weightInKilograms >= 0"))
    birthDate: so.Mapped[date] = so.mapped_column()
    birthCity: so.Mapped[str] = so.mapped_column(nullable=True)
    birthCountry: so.Mapped[str] = so.mapped_column()
    shootsCatches: so.Mapped[str] = so.mapped_column(sa.CheckConstraint('''shootsCatches IN ("L","R")'''))
    draftYear: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftYear > 0"), nullable=True)
    draftTeamAbbrev: so.Mapped[str] = so.mapped_column(nullable=True)
    draftRound: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftRound > 0"), nullable=True)
    draftPickInRound: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftPickInRound > 0"), nullable=True)
    draftOverallPick: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("draftOverallPick > 0"), nullable=True)
    inHHOF: so.Mapped[bool] = so.mapped_column(nullable=True, default=0)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    team: so.Mapped[Team] = so.relationship(back_populates='players')
    awards: so.Mapped[list['Award']] = so.relationship(back_populates='winningPlayer', foreign_keys='Award.winningPlayerID')

    def __repr__(self):
        return f"Player: {self.firstName} {self.lastName} <{self.id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'isActive': self.isActive,
            'currentTeamID': self.currentTeamID,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'sweaterNumber': self.sweaterNumber,
            'position': self.position,
            'headshot': self.headshot,
            'heroImage': self.heroImage,
            'heightInInches': self.heightInInches,
            'heightInCentimeters': self.heightInCentimeters,
            'weightInPounds': self.weightInPounds,
            'weightInKilograms': self.weightInKilograms,
            'birthDate': self.birthDate,
            'birthCity': self.birthCity,
            'birthCountry': self.birthCountry,
            'shootsCatches': self.shootsCatches,
            'draftYear': self.draftYear,
            'draftTeamAbbrev': self.draftTeamAbbrev,
            'draftRound': self.draftRound,
            'draftPickInRound': self.draftPickInRound,
            'draftOverallPick': self.draftOverallPick,
            'inHHOF': self.inHHOF,
            'team': self.team.to_dict() if self.team else None,
            'awards': [award.to_dict() for award in self.awards]
        }
    
    def get_list_item(self) -> PlayerListItem:
        try:
            return PlayerListItem(
                id=self.id,
                fullName=f'{self.firstName} {self.lastName}',
                position=self.position,
                teamTriCode=self.team.triCode if self.team else None,
                headshot=self.headshot
            )
        except ValidationError as e:
            # app.logger.error(f'{self} failed PlayerListItem Validation')
            # app.logger.error(e)
            return None
    
    def goals(self) -> int:
        return Event.query.filter(Event.scoringPlayerID == self.id).count()
    
    def primaryAssists(self) -> int:
        return Event.query.filter(Event.assist1PlayerID == self.id).count()
    
class Award(db.Model):
    __tablename__ = 'awards'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    awardName: so.Mapped[str] = so.mapped_column()
    season: so.Mapped[int] = so.mapped_column()
    winningPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))

    winningPlayer: so.Mapped[Player] = so.relationship(back_populates='awards')

    def __eq__(self, other):
        if isinstance(other, Award):
            return (self.awardName == other.awardName and self.season == other.season)
        return False
    
    def __hash__(self):
        return hash(str(self.season) + self.awardName)

    def to_dict(self):
        return {
            'awardName':self.awardName,
            'season':self.season
        }

class GameType(db.Model):
    __tablename__ = "game_types"

    typeCode: so.Mapped[int] = so.mapped_column(primary_key=True)
    typeDescKey: so.Mapped[str] = so.mapped_column()

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
    season: so.Mapped[int] = so.mapped_column(index=True)
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

    homeTeam: so.Mapped[Team] = so.relationship(back_populates='homeGames', foreign_keys=[homeTeamID])
    awayTeam: so.Mapped[Team] = so.relationship(back_populates='awayGames', foreign_keys=[awayTeamID])
    events: so.Mapped[list['Event']] = so.relationship(back_populates='game', foreign_keys='Event.gameID')

    def to_dict(self):
        return {
            'id': self.id,
            'season': self.season,
            'gameType': self.gameType,
            'neutralSite': self.neutralSite,
            'startTimeUTC': self.startTimeUTC,
            'venueUTCOffset': self.venueUTCOffset,
            'gameState': self.gameState,
            'gameScheduleState': self.gameScheduleState,
            'defaultVenue': self.defaultVenue,
            'awayTeamID': self.awayTeamID,
            'awayTeamScore': self.awayTeamScore,
            'homeTeamID': self.homeTeamID,
            'homeTeamScore': self.homeTeamScore,
            'maxRegulationPeriods': self.maxRegulationPeriods,
            'lastPeriodType': self.lastPeriodType
        }
    
    def __repr__(self):
        if self.homeTeam is not None and self.awayTeam is not None:
            return f"Game: <{self.awayTeam.fullName} @ {self.homeTeam.fullName} {self.startTimeUTC}>"
        else:
            return f"Game: <{self.awayTeamID} @ {self.homeTeamID} {self.startTimeUTC}>"
    

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
    timeInPeriodSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("timeInPeriodSec >= 0"), nullable=True)
    awayGoalie: so.Mapped[int] = so.mapped_column(nullable=True)
    awaySkaters: so.Mapped[int] = so.mapped_column(nullable=True)
    homeGoalie: so.Mapped[int] = so.mapped_column(nullable=True)
    homeSkaters: so.Mapped[int] = so.mapped_column(nullable=True)
    homeTeamDefendingSide: so.Mapped[str] = so.mapped_column(nullable=True)
    typeCode: so.Mapped[int] = so.mapped_column(sa.ForeignKey(EventType.typeCode), index=True)
    sortOrder: so.Mapped[int] = so.mapped_column(nullable=True)
    period: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("period > 0"), nullable=True)
    periodType: so.Mapped[str] = so.mapped_column(nullable=True)
    eventOwnerTeamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), nullable=True, index=True)
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    losingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    winningPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    xCoord: so.Mapped[float] = so.mapped_column(nullable=True)
    yCoord: so.Mapped[float] = so.mapped_column(nullable=True)
    zoneCode: so.Mapped[str] = so.mapped_column(nullable=True)
    hittingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    hitteePlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    blockingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    shootingPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    reason: so.Mapped[str] = so.mapped_column(nullable=True)
    shotType: so.Mapped[str] = so.mapped_column(nullable=True)
    goalieInNetID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    eventOwnerPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    duration: so.Mapped[int] = so.mapped_column(nullable=True)
    committedByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    drawnByPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    scoringPlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    assist1PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    assist2PlayerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), nullable=True, index=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), primary_key=True, index=True)
    xg: so.Mapped[float] = so.mapped_column(nullable = True)
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

    game: so.Mapped['Game'] = so.relationship(back_populates='events')

    def __repr__(self):
        return f"<Event: {self.typeCode}>"
    

class Shift(db.Model, Util):
    __tablename__ = "shifts"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    durationSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("durationSec >= 0"))
    startTimeSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("startTimeSec >= 0"))
    endTimeSec: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("endTimeSec >= 0"))
    eventNumber: so.Mapped[int] = so.mapped_column(nullable=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id))
    period: so.Mapped[int] = so.mapped_column(sa.CheckConstraint("period > 0"))
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    shiftNumber: so.Mapped[int] = so.mapped_column()
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    metaDateTime: so.Mapped[datetime] = so.mapped_column(default = lambda: datetime.now(timezone.utc))

class SplitShift(db.Model):
    __tablename__ = "split_shifts"

    shiftID: so.Mapped[int] = so.mapped_column(primary_key=True)
    split: so.Mapped[int] = so.mapped_column(primary_key=True)
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id))
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id))
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id))
    period: so.Mapped[int] = so.mapped_column()
    startTimeSec: so.Mapped[int] = so.mapped_column()
    endTimeSec: so.Mapped[int] = so.mapped_column()
    splitDuration: so.Mapped[int] = so.mapped_column()
    attackingSkaters: so.Mapped[int] = so.mapped_column()
    defendingSkaters: so.Mapped[int] = so.mapped_column()
    attackingGoalie: so.Mapped[bool] = so.mapped_column()
    defendingGoalie: so.Mapped[bool] = so.mapped_column()
    goalsFor: so.Mapped[int] = so.mapped_column()
    goalsAgainst: so.Mapped[int] = so.mapped_column()
    sogFor: so.Mapped[int] = so.mapped_column()
    sogAgainst: so.Mapped[int] = so.mapped_column()
    fenwickFor: so.Mapped[int] = so.mapped_column()
    fenwickAgainst: so.Mapped[int] = so.mapped_column()
    corsiFor: so.Mapped[int] = so.mapped_column()
    corsiAgainst: so.Mapped[int] = so.mapped_column()
    xgFor: so.Mapped[float] = so.mapped_column()
    xgAgainst: so.Mapped[float] = so.mapped_column()
    dZoneStarts: so.Mapped[int] = so.mapped_column()
    nZoneStarts: so.Mapped[int] = so.mapped_column()
    oZoneStarts: so.Mapped[int] = so.mapped_column()
    
class GoalieAppearance(db.Model, Util):
    __tablename__ = "goalie_appearances"

    appearanceID: so.Mapped[int] = so.mapped_column(primary_key=True)
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), index=True)
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), index=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), index=True)
    evenStrengthSaves: so.Mapped[int] = so.mapped_column()
    evenStrengthShotsAgainst: so.Mapped[int] = so.mapped_column()
    powerPlaySaves: so.Mapped[int] = so.mapped_column()
    powerPlayShotsAgainst: so.Mapped[int] = so.mapped_column()
    shorthandedSaves: so.Mapped[int] = so.mapped_column()
    shorthandedShotsAgainst: so.Mapped[int] = so.mapped_column()
    saves: so.Mapped[int] = so.mapped_column()
    shotsAgainst: so.Mapped[int] = so.mapped_column()
    toiSeconds: so.Mapped[int] = so.mapped_column()
    starter: so.Mapped[bool] = so.mapped_column()
    played: so.Mapped[bool] = so.mapped_column()
    decision: so.Mapped[str] = so.mapped_column(nullable=True)

class SkaterAppearance(db.Model):
    __tablename__ = "skater_appearances"

    appearanceID: so.Mapped[int] = so.mapped_column(primary_key=True)
    playerID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Player.id), index=True)
    teamID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Team.id), index=True)
    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), index=True)
    position: so.Mapped[str] = so.mapped_column(nullable=True)
    goals: so.Mapped[int] = so.mapped_column()
    powerPlayGoals: so.Mapped[int] = so.mapped_column()
    assists: so.Mapped[int] = so.mapped_column()
    plusMinus: so.Mapped[int] = so.mapped_column()
    pim: so.Mapped[int] = so.mapped_column()
    hits: so.Mapped[int] = so.mapped_column()
    sog: so.Mapped[int] = so.mapped_column()
    blocks: so.Mapped[int] = so.mapped_column()
    giveaways: so.Mapped[int] = so.mapped_column()
    takeaways: so.Mapped[int] = so.mapped_column()
    toiSeconds: so.Mapped[int] = so.mapped_column()
    
class GameImportError(db.Model):
    __tablename__ = "game_import_errors"

    gameID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Game.id), primary_key=True)
    reason: so.Mapped[str] = so.mapped_column()

    def __init__(self, gameID: int, reason: str):
        self.gameID = gameID
        self.reason = reason