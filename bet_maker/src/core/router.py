from decimal import Decimal
from urllib.parse import urljoin

import httpx
import pydantic
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from core.schema import BetCallback, BetSchema, BetSchemaOut, Event, MakeBet
from db.models.betshistory import Bet
from dependencies import get_async_client, get_session, validate_credentials
from settings import auth_settings, service_urls

router = APIRouter(tags=["Main"])


@router.get("/events/", response_model=list[Event])
async def event_list(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> list[Event]:
    response = await async_client.get(
        urljoin(
            service_urls.url_base,
            f"/event/active/",
        ),
        headers={"inner-key": auth_settings.inner_key},
    )
    response.raise_for_status()
    return pydantic.parse_obj_as(list[Event], response.json())


@router.post("/bet/{event_id}/", response_model=BetSchemaOut)
async def create_bet(
    event_id: int,
    postdata: MakeBet,
    async_client: httpx.AsyncClient = Depends(get_async_client),
    session: AsyncSession = Depends(get_session),
) -> Bet:
    response = await async_client.post(
        urljoin(
            service_urls.url_base,
            f"/event/bet/{event_id}/",
        ),
        headers={"inner-key": auth_settings.inner_key},
        data=postdata.json(),
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Bet cancelled")

    response_data: BetSchema = BetSchema.parse_obj(response.json())
    bet = Bet(
        event_id=response_data.event_id,
        deadline=response_data.deadline,
        state=response_data.state,
        coefficient=response_data.coefficient,
        bet_amount=Decimal(postdata.bet_amount),
    )
    session.add(bet)
    await session.commit()
    await session.refresh(bet)
    return bet


@router.post(
    "/callback/bet/{event_id}/",
    response_model=BetSchemaOut,
    dependencies=[Depends(validate_credentials)],
)
async def callback(
    event_id: int,
    postdata: BetCallback,
    session: AsyncSession = Depends(get_session),
) -> None:
    bet: Bet | None = await session.get(Bet, event_id)
    if bet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    bet.win_amount = Decimal(postdata.win_amount)
    bet.state = postdata.state

    session.add(bet)
    await session.commit()
    await session.refresh(bet)


@router.get("/bets/", response_model=list[BetSchema])
async def bet_list(
    session: AsyncSession = Depends(get_session),
) -> list[BetSchema]:
    bets = list(await session.scalars(select(Bet)))
    return bets
