import datetime
import enum
from decimal import Decimal
from enum import Enum

from pydantic import validator

from app.base_schema import BaseSchema


class EventState(Enum):
    NEW = enum.auto()
    WIN = enum.auto()
    LOSE = enum.auto()
    BOOKED = enum.auto()


class Event(BaseSchema):
    event_id: int
    coefficient: float
    deadline: datetime.datetime
    state: EventState
    bet_amount: Decimal | None = None
    win_amount: Decimal | None = None


class CreateEvent(BaseSchema):
    coefficient: Decimal
    deadline: datetime.datetime

    @validator("coefficient")
    def valid_coefficient(cls, v: Decimal) -> Decimal:
        if v > 0:
            return v
        raise ValueError("Coefficient less than or equal to zero")

    @validator("deadline")
    def valid_deadline(cls, v: datetime.datetime) -> datetime.datetime:
        if v > datetime.datetime.now() + datetime.timedelta(minutes=1):
            return v
        raise ValueError("Deadline's too close to the current datetime")


class UpdateEvent(CreateEvent):
    state: EventState | None = None
    coefficient: Decimal | None = None
    win_amount: float | None = None


class MakeBet(BaseSchema):
    bet_amount: float | None
