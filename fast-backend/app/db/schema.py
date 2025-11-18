from typing import Optional, List
from datetime import date, datetime, timezone

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from app.models.players import PlayerRead, PlayerListItem, AwardBase
from app.models.teams import TeamBase
from app.models.games import GameBase

class Player(Base):
    __tablename__ = 'players'
                     
    id: Mapped[int] = mapped_column(primary_key=True)
    isActive: Mapped[bool] = mapped_column()
    currentTeamID: Mapped[Optional[int]] = mapped_column(ForeignKey('teams.id'))
    firstName: Mapped[str] = mapped_column()
    lastName: Mapped[str] = mapped_column()
    sweaterNumber: Mapped[Optional[int]] = mapped_column()
    position: Mapped[str] = mapped_column()
    headshot: Mapped[Optional[str]] = mapped_column()
    heightInInches: Mapped[Optional[int]] = mapped_column()
    heightInCentimeters: Mapped[Optional[int]] = mapped_column()
    weightInPounds: Mapped[Optional[int]] = mapped_column()
    weightInKilograms: Mapped[Optional[int]] = mapped_column()
    birthDate: Mapped[date] = mapped_column()
    birthCountry: Mapped[str] = mapped_column()
    shootsCatches: Mapped[str] = mapped_column()
    draftYear: Mapped[Optional[int]] = mapped_column()
    draftTeamAbbrev: Mapped[Optional[str]] = mapped_column()
    draftRound: Mapped[Optional[int]] = mapped_column()
    draftPickInRound: Mapped[Optional[int]] = mapped_column()
    draftOverallPick: Mapped[Optional[int]] = mapped_column()
    inHHOF: Mapped[Optional[bool]] = mapped_column(nullable=True, default=False)
    metaDateTime: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    team: Mapped['Team'] = relationship('Team', back_populates='players')
    awards: Mapped[List['Award']] = relationship(
        'Award',
        back_populates='winningPlayer',
        cascade="all, delete"
    )

    def __repr__(self):
        return f"Player <{self.id}>: {self.firstName} {self.lastName}"
    
    async def get_team_to_read(self) -> TeamBase:
        team: Team | None = await self.awaitable_attrs.team
        if team is None:
            return None
        else:
            return team.to_read()
    
    async def to_read(self) -> PlayerRead:
        return PlayerRead(
            id=self.id,
            isActive=self.isActive,
            currentTeamID=self.currentTeamID,
            firstName=self.firstName,
            lastName=self.lastName,
            sweaterNumber=self.sweaterNumber,
            position=self.position,
            headshot=self.headshot,
            heightInInches=self.heightInInches,
            heightInCentimeters=self.heightInCentimeters,
            weightInPounds=self.weightInPounds,
            weightInKilograms=self.weightInKilograms,
            birthDate=self.birthDate.strftime('%m-%d-%Y'),
            birthCountry=self.birthCountry,
            shootsCatches=self.shootsCatches,
            draftYear=self.draftYear,
            draftTeamAbbrev=self.draftTeamAbbrev,
            draftRound=self.draftRound,
            draftPickInRound=self.draftPickInRound,
            draftOverallPick=self.draftOverallPick,
            inHHOF=self.inHHOF,
            team=await self.get_team_to_read(),
            awards=[award.to_read() for award in await self.awaitable_attrs.awards]
        )
    
    async def to_list_item(self) -> PlayerListItem:
        return PlayerListItem(
            id=self.id,
            fullName=f"{self.firstName} {self.lastName}",
            isActive=self.isActive,
            position=self.position,
            teamTriCode= await self.awaitable_attrs.team.triCode if self.currentTeamID else None,
            headshot=self.headshot
        )
    

class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    franchiseID: Mapped[Optional[int]] = mapped_column()
    fullName: Mapped[str] = mapped_column()
    triCode: Mapped[str] = mapped_column()
    metaDateTime: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    players: Mapped[List['Player']] = relationship('Player', back_populates='team')

    def __repr__(self):
        return f"Team <{self.id}>: {self.fullName}"
    
    def to_read(self):
        return TeamBase(
            id=self.id,
            franchiseID=self.franchiseID,
            fullName=self.fullName,
            triCode=self.triCode
        )


class Award(Base):
    __tablename__ = 'awards'
    __table_args__ = (UniqueConstraint("awardName", "season", name='awards_constraint'),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    awardName: Mapped[str] = mapped_column()
    season: Mapped[int] = mapped_column(index=True)
    winningPlayerID: Mapped[int] = mapped_column(ForeignKey('players.id'))

    winningPlayer: Mapped['Player'] = relationship('Player', back_populates='awards')

    def __repr__(self):
        return f"Award <{self.id}>: {self.season} {self.awardName}"
    
    def to_read(self):
        return AwardBase(
            awardName=self.awardName,
            season=self.season,
            winningPlayerID=self.winningPlayerID
        )
    

class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[int] = mapped_column(index=True)
    gameType: Mapped[int] = mapped_column(index=True)
    neutralSite: Mapped[bool] = mapped_column()
    gameDate: Mapped[date] = mapped_column()
    defaultVenue: Mapped[str] = mapped_column()
    awayTeamID: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    awayTeamScore: Mapped[int] = mapped_column()
    homeTeamID: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    homeTeamScore: Mapped[int] = mapped_column()
    lastPeriodType: Mapped[str] = mapped_column()
    metaDateTime: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    events: Mapped[List['Event']] = relationship(
        'Event',
        back_populates='game',
        cascade='all, delete'
    )
    shifts: Mapped[List['Shift']] = relationship(
        'Shift',
        back_populates='game',
        cascade='all, delete'
    )
    splitShifts: Mapped[List['SplitShift']] = relationship(
        'SplitShift',
        back_populates='game',
        cascade='all, delete'
    )
    goalieAppearances: Mapped[List['GoalieAppearance']] = relationship(
        'GoalieAppearance',
        back_populates='game',
        cascade='all, delete'
    )
    skaterAppearances: Mapped[List['SkaterAppearance']] = relationship(
        'SkaterAppearance',
        back_populates='game',
        cascade='all, delete'
    )

    def __repr__(self):
        return f"Game <{self.id}>: {self.awayTeamID} @ {self.homeTeamID} ({self.gameDate})"
    
    def to_read(self):
        return GameBase(
            id=self.id,
            season=self.season,
            gameType=self.gameType,
            neutralSite=self.neutralSite,
            gameDate=self.gameDate.strftime('%m-%d-%Y'),
            defaultVenue=self.defaultVenue,
            awayTeamID=self.awayTeamID,
            homeTeamID=self.homeTeamID,
            homeTeamScore=self.homeTeamScore,
            awayTeamScore=self.awayTeamScore,
            lastPeriodType=self.lastPeriodType
        )


class EventType(Base):
    __tablename__ = "event_types"

    typeCode: Mapped[int] = mapped_column(primary_key=True)
    typeDescKey: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"EventType <{self.typeCode}>: {self.typeDescKey}"
    

class Event(Base):
    __tablename__ = "events"

    eventID: Mapped[int] = mapped_column(primary_key=True)
    gameID: Mapped[int] = mapped_column(ForeignKey('games.id'), primary_key=True, index=True)
    timeInPeriodSec: Mapped[int] = mapped_column()
    awayScore: Mapped[Optional[int]] = mapped_column()
    homeScore: Mapped[Optional[int]] = mapped_column()
    awayGoalie: Mapped[Optional[int]] = mapped_column()
    awaySkaters: Mapped[Optional[int]] = mapped_column()
    homeGoalie: Mapped[Optional[int]] = mapped_column()
    homeSkaters: Mapped[Optional[int]] = mapped_column()
    homeTeamDefendingSide: Mapped[Optional[str]] = mapped_column()
    typeCode: Mapped[int] = mapped_column(ForeignKey('event_types.typeCode'), index=True)
    sortOrder: Mapped[Optional[int]] = mapped_column()
    period: Mapped[int] = mapped_column()
    periodType: Mapped[Optional[str]] = mapped_column()
    eventOwnerTeamID: Mapped[Optional[int]] = mapped_column(ForeignKey('teams.id'), index=True)
    losingPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    winningPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    xCoord: Mapped[Optional[float]] = mapped_column()
    yCoord: Mapped[Optional[float]] = mapped_column()
    xStd: Mapped[Optional[float]] = mapped_column()
    yStd: Mapped[Optional[float]] = mapped_column()
    zoneCode: Mapped[Optional[str]] = mapped_column()
    hittingPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    hitteePlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    blockingPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    shootingPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    shotType: Mapped[Optional[str]] = mapped_column()
    goalieInNetID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    eventOwnerPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    duration: Mapped[Optional[int]] = mapped_column()
    committedByPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    drawnByPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    scoringPlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    assist1PlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    assist2PlayerID: Mapped[Optional[int]] = mapped_column(ForeignKey('players.id'), index=True)
    xg: Mapped[Optional[float]] = mapped_column()
    highlightClipSharingURL: Mapped[Optional[str]] = mapped_column()

    game: Mapped['Game'] = relationship('Game', back_populates='events')
    

class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    gameID: Mapped[int] = mapped_column(ForeignKey('games.id'), index=True)
    playerID: Mapped[int] = mapped_column(ForeignKey('players.id'), index=True)
    teamID: Mapped[int] = mapped_column(ForeignKey('teams.id'), index=True)
    durationSec: Mapped[int] = mapped_column()
    startTimeSec: Mapped[int] = mapped_column()
    endTimeSec: Mapped[int] = mapped_column()
    period: Mapped[int] = mapped_column()
    shiftNumber: Mapped[int] = mapped_column()

    game: Mapped['Game'] = relationship('Game', back_populates='shifts')

class SplitShift(Base):
    __tablename__ = "split_shifts"

    shiftID: Mapped[int] = mapped_column(primary_key=True)
    split: Mapped[int] = mapped_column(primary_key=True)
    teamID: Mapped[int] = mapped_column(ForeignKey('teams.id'), index=True)
    playerID: Mapped[int] = mapped_column(ForeignKey('players.id'), index=True)
    gameID: Mapped[int] = mapped_column(ForeignKey('games.id'), index=True)
    period: Mapped[int] = mapped_column()
    startTimeSec: Mapped[int] = mapped_column()
    endTimeSec: Mapped[int] = mapped_column()
    splitDuration: Mapped[int] = mapped_column()
    attackingSkaters: Mapped[int] = mapped_column()
    defendingSkaters: Mapped[int] = mapped_column()
    attackingGoalie: Mapped[bool] = mapped_column()
    defendingGoalie: Mapped[bool] = mapped_column()
    goalsFor: Mapped[int] = mapped_column()
    goalsAgainst: Mapped[int] = mapped_column()
    sogFor: Mapped[int] = mapped_column()
    sogAgainst: Mapped[int] = mapped_column()
    fenwickFor: Mapped[int] = mapped_column()
    fenwickAgainst: Mapped[int] = mapped_column()
    corsiFor: Mapped[int] = mapped_column()
    corsiAgainst: Mapped[int] = mapped_column()
    xgFor: Mapped[float] = mapped_column()
    xgAgainst: Mapped[float] = mapped_column()
    dZoneStarts: Mapped[int] = mapped_column()
    nZoneStarts: Mapped[int] = mapped_column()
    oZoneStarts: Mapped[int] = mapped_column()

    game: Mapped['Game'] = relationship('Game', back_populates='splitShifts')


class GoalieAppearance(Base):
    __tablename__ = "goalie_appearances"

    playerID: Mapped[int] = mapped_column(ForeignKey('players.id'), primary_key=True, index=True)
    gameID: Mapped[int] = mapped_column(ForeignKey('games.id'), primary_key=True, index=True)
    teamID: Mapped[int] = mapped_column(ForeignKey('teams.id'), index=True)
    evenStrengthSaves: Mapped[int] = mapped_column()
    evenStrengthShotsAgainst: Mapped[int] = mapped_column()
    powerPlaySaves: Mapped[int] = mapped_column()
    powerPlayShotsAgainst: Mapped[int] = mapped_column()
    shorthandedSaves: Mapped[int] = mapped_column()
    shorthandedShotsAgainst: Mapped[int] = mapped_column()
    saves: Mapped[int] = mapped_column()
    shotsAgainst: Mapped[int] = mapped_column()
    toiSeconds: Mapped[int] = mapped_column()
    starter: Mapped[bool] = mapped_column()
    played: Mapped[bool] = mapped_column()
    decision: Mapped[Optional[str]] = mapped_column()

    game: Mapped['Game'] = relationship('Game', back_populates='goalieAppearances')

class SkaterAppearance(Base):
    __tablename__ = "skater_appearances"

    appearanceID: Mapped[int] = mapped_column(primary_key=True)
    playerID: Mapped[int] = mapped_column(ForeignKey('players.id'), index=True)
    teamID: Mapped[int] = mapped_column(ForeignKey('teams.id'), index=True)
    gameID: Mapped[int] = mapped_column(ForeignKey('games.id'), index=True)
    position: Mapped[str] = mapped_column()
    goals: Mapped[int] = mapped_column()
    powerPlayGoals: Mapped[int] = mapped_column()
    assists: Mapped[int] = mapped_column()
    plusMinus: Mapped[int] = mapped_column()
    pim: Mapped[int] = mapped_column()
    hits: Mapped[int] = mapped_column()
    sog: Mapped[int] = mapped_column()
    blocks: Mapped[int] = mapped_column()
    giveaways: Mapped[int] = mapped_column()
    takeaways: Mapped[int] = mapped_column()
    toiSeconds: Mapped[int] = mapped_column()

    game: Mapped['Game'] = relationship('Game', back_populates='skaterAppearances')