import datetime
import enum
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import validator

from app.base_schema import BaseSchema


class EventState(Enum):
    NEW = enum.auto()
    WIN = enum.auto()
    LOSE = enum.auto()


class Event(BaseSchema):
    event_id: int
    coefficient: Decimal
    deadline: datetime.datetime
    state: EventState

    @validator("state")
    def pretty_state(cls, v: EventState) -> str:
        return v.name


class BetSchema(BaseSchema):
    event_id: int
    coefficient: Decimal
    deadline: datetime.datetime
    state: str


class BetSchemaOut(BetSchema):
    id: UUID
    bet_amount: float | None
    win_amount: float | None


class MakeBet(BaseSchema):
    bet_amount: float


class BetCallback(BaseSchema):
    win_amount: float
    state: EventState

    @validator("state")
    def pretty_state(cls, v: EventState) -> str:
        return v.name
