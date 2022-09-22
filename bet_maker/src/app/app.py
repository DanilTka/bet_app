from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from core.router import router
from dependencies import get_session


def create_app() -> FastAPI:
    app = FastAPI(title="Bet maker")
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
    )

    app.include_router(router)

    @app.get("/db_healthcheck")
    def healthcheck(session: AsyncSession = Depends(get_session)) -> None:
        pass

    return app
