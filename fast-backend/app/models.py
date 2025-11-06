from typing import Optional
from datetime import date, datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Player(Base):
    __tablename__ = 'players'
                     
    id: Mapped[int] = mapped_column(primary_key=True)
    isActive: Mapped[bool] = mapped_column()
    currentTeamID: Mapped[Optional[int]] = mapped_column(nullable=True)
    firstName: Mapped[str] = mapped_column()
    lastName: Mapped[str] = mapped_column()
    sweaterNumber: Mapped[Optional[int]] = mapped_column(nullable=True)
    position: Mapped[str] = mapped_column()
    headshot: Mapped[Optional[str]] = mapped_column(nullable=True)
    heightInInches: Mapped[Optional[int]] = mapped_column(nullable=True)
    heightInCentimeters: Mapped[Optional[int]] = mapped_column(nullable=True)
    weightInPounds: Mapped[Optional[int]] = mapped_column(nullable=True)
    weightInKilograms: Mapped[Optional[int]] = mapped_column(nullable=True)
    birthDate: Mapped[date] = mapped_column()
    birthCountry: Mapped[str] = mapped_column()
    shootsCatches: Mapped[str] = mapped_column()
    draftYear: Mapped[Optional[int]] = mapped_column(nullable=True)
    draftTeamAbbrev: Mapped[Optional[str]] = mapped_column(nullable=True)
    draftRound: Mapped[Optional[int]] = mapped_column(nullable=True)
    draftPickInRound: Mapped[Optional[int]] = mapped_column(nullable=True)
    draftOverallPick: Mapped[Optional[int]] = mapped_column(nullable=True)
    inHHOF: Mapped[Optional[bool]] = mapped_column(nullable=True, default=0)
    metaDateTime: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"Player <{self.id}>: {self.firstName} {self.lastName}"
