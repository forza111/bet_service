import decimal
import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, CheckConstraint, TIMESTAMP, ForeignKey

from src.db.database import Base
from src.schemas.event import EventState
from src.schemas.bet import MatchOutcome


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    state: Mapped[EventState]
    coefficient: Mapped[decimal] = mapped_column(Numeric(32, 2))

    bet: Mapped[list["Bet"]] = relationship(back_populates='event')
    __table_args__ = (
        CheckConstraint("coefficient > 0"),
    )


class Bet(Base):
    __tablename__ = 'bet'

    id: Mapped[int] = mapped_column(primary_key=True)
    bet_amount: Mapped[decimal] = mapped_column(Numeric(32, 2))
    amount_of_winnings: Mapped[decimal] = mapped_column(
        Numeric(32, 2),
        nullable=True
    )
    match_outcome: Mapped[MatchOutcome]
    coefficient: Mapped[decimal] = mapped_column(Numeric(32, 2))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    event: Mapped["Event"] = relationship(back_populates='bet')

    __table_args__ = (
        CheckConstraint("coefficient > 0"),
        CheckConstraint("bet_amount > 0"),
    )
