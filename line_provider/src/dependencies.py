import hmac

import httpx
from fastapi import HTTPException, Header
from starlette.status import HTTP_403_FORBIDDEN

from httpx_client import async_client
from settings import auth_settings


def get_api_key(
    api_key: str,
) -> str:
    if hmac.compare_digest(api_key, auth_settings.api_key):
        return api_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


def validate_credentials(
    inner_key: str = Header(default=""),
) -> str:
    if hmac.compare_digest(inner_key, auth_settings.inner_key):
        return inner_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


def get_async_client() -> httpx.AsyncClient:
    return async_client
