from fastapi import FastAPI

from catboys.app.routes import router
from catboys.db import base, engine


def make_app():
    app = FastAPI(
        name="catboys",
    )

    app.include_router(router)

    @app.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(base.Base.metadata.create_all)

    return app
