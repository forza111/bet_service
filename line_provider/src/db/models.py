import decimal
import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, CheckConstraint, TIMESTAMP

from src.db.database import Base
from src.schemas.event import EventState


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    coefficient: Mapped[decimal] = mapped_column(Numeric(32, 2))
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    state: Mapped[EventState]

    __table_args__ = (
        CheckConstraint("coefficient > 0"),
    )
