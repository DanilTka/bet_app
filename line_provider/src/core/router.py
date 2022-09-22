from decimal import Decimal
from urllib.parse import urljoin

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.loguru_settings import line_logger
from core.data import INNER_EVENTS
from core.schema import Event, CreateEvent, EventState, UpdateEvent, MakeBet
from core.service import get_active_events
from dependencies import validate_credentials, get_async_client, get_api_key
from settings import service_urls, auth_settings

router = APIRouter(tags=["Main"], prefix="/event")


@router.get("/{event_id}/", response_model=Event)
async def get_event(event_id: int):
    if event := INNER_EVENTS.get(event_id):
        return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.get(
    "/closed/", response_model=list[Event],
    )
async def event_list():
    closed: list[Event] = []
    for event in INNER_EVENTS.values():
        if event.state in [EventState.WIN, EventState.LOSE]:
            closed.append(event)
    if closed:
        return closed
    raise HTTPException(status_code=404, detail="Events not found")


@router.post("/", response_model=Event, dependencies=[Depends(get_api_key)])
async def create_event(event: CreateEvent):
    next_id: int = sorted(INNER_EVENTS.keys()).pop() + 1
    INNER_EVENTS.update(
        {
            next_id: Event(
                event_id=next_id, coefficient=event.coefficient,
                deadline=event.deadline, state=EventState.NEW
            )
        }
    )

    return INNER_EVENTS[next_id]


@router.patch("/{event_id}/", response_model=Event, dependencies=[Depends(get_api_key)])
async def update_event(
        event_id: int, event: UpdateEvent, async_client: httpx.AsyncClient = Depends(
            get_async_client
        ),
):
    if saved_event := INNER_EVENTS.get(event_id):
        data_to_update = event.dict(exclude_unset=True)
        for data in data_to_update.items():
            setattr(saved_event, data[0], data[1])

        response = await async_client.post(
            urljoin(
                service_urls.url_base,
                f"/callback/bet/{event_id}/",
            ),
            headers={"inner-key": auth_settings.inner_key},
            data=event.json(),
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to deliver bet update date")

        return saved_event
    raise HTTPException(status_code=404, detail="Event not found")


@router.get(
    "/active/", response_model=list[Event], dependencies=[Depends(validate_credentials)],
)
async def active_event():
    if events := INNER_EVENTS.values():
        active_events: list[Event] = get_active_events(events)
        line_logger.info(f"{active_events=}")
        return active_events
    raise HTTPException(status_code=404, detail="Events not found")


@router.get(
    "/history/", response_model=list[Event], dependencies=[Depends(validate_credentials)],
)
async def event_list():
    if events := INNER_EVENTS.values():
        return list(events)
    raise HTTPException(status_code=404, detail="Events not found")


@router.post(
    "/bet/{event_id}/", response_model=Event, dependencies=[Depends(validate_credentials)],
)
async def process_bet(event_id: int, postdata: MakeBet):
    if events := INNER_EVENTS.values():
        active_events: list[Event] = get_active_events(events)
        if requested := list(filter(lambda ev: (ev.event_id == event_id), active_events)):
            requested_event = requested[0]
            requested_event.state = EventState.BOOKED
            requested_event.bet_amount = Decimal(postdata.bet_amount)
            return requested_event
    raise HTTPException(status_code=404, detail="Event not found")
