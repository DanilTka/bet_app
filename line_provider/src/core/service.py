import datetime

from core.schema import Event, EventState


def get_active_events(events: list[Event]):
    return list(
        filter(
            lambda ev: (ev.state == EventState.NEW) and (ev.deadline >
                                                         datetime.datetime.now()), events
            )
        )
