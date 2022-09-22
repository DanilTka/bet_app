import datetime
import random
import uuid

from core.schema import Event, EventState

INNER_EVENTS: dict[uuid.UUID, Event] = {
    1: Event(
        event_id=1, coefficient=random.uniform(1, 10),
        deadline=datetime.datetime.now() +
                 datetime.timedelta(
                     minutes=random.randrange(1, 100)
                 ), state=EventState.NEW
    ),
    2: Event(
        event_id=2, coefficient=random.uniform(1, 10),
        deadline=datetime.datetime.now() +
                 datetime.timedelta(
                     minutes=random.randrange(1, 100)
                 ), state=EventState.WIN
    ),
    3: Event(
        event_id=3, coefficient=random.uniform(1, 10),
        deadline=datetime.datetime.now() +
                 datetime.timedelta(
                     minutes=random.randrange(1, 100)
                 ), state=EventState.LOSE
    )
}
