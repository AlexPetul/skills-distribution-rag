from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.controllers.api.router import router
from app.infrastructure.persistence.models import map_all_tables
from app.setup.ioc.provider import ApplicationProvider


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    map_all_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

container = make_async_container(ApplicationProvider())
setup_dishka(container, app)
