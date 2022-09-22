from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.router import router


def create_app() -> FastAPI:
    app = FastAPI(title="Line provider")
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
    )

    app.include_router(router)

    return app
