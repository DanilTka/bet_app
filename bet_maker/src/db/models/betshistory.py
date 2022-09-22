from __future__ import annotations

import datetime
import uuid
from decimal import Decimal
from functools import partial

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from db import Base


class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[int] = Column(Integer())
    bet_amount: Mapped[Decimal] = Column(Numeric(precision=14, scale=4))
    win_amount: Mapped[Decimal] = Column(Numeric(precision=14, scale=4), nullable=True)
    state: Mapped[str] = Column(String(length=10))
    deadline: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=partial(datetime.datetime.now, datetime.timezone.utc),
    )
    coefficient: Mapped[Decimal] = Column(Numeric(precision=14, scale=4))
