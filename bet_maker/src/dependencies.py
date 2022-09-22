import hmac
from typing import AsyncGenerator

import httpx
from fastapi import Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

import db
from httpx_client import async_client
from settings import auth_settings


def get_async_client() -> httpx.AsyncClient:
    return async_client


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.base.Session() as session:
        yield session


def validate_credentials(
    inner_key: str = Header(default=""),
) -> str:
    if hmac.compare_digest(inner_key, auth_settings.inner_key):
        return inner_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
