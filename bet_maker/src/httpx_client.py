import httpx

_timeout = httpx.Timeout(
    timeout=5.0,
)
async_client = httpx.AsyncClient(timeout=_timeout)
