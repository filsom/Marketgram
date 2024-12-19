from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI
import uvicorn

from marketgram.identity.access.ioc import (
    DatabaseProvider, 
    EmailMessageProvider, 
    HTTPProvider, 
    HandlerProvider,
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_identity_mapper import (
    identity_registry_mapper,
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_identity_table import (
    metadata
)
from marketgram.identity.access.port.adapter.web_fastapi.router import router
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import registry

from dishka import make_async_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    # engine = create_async_engine(
    #         '', echo=True
    #     )
    # async with engine.begin() as s:
    #     await s.run_sync(metadata.create_all)
    #     await s.commit()

    # mapper_registry = registry()
    # identity_registry_mapper(mapper_registry)

    yield

    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


def create_app(app):
    container = make_async_container(
        DatabaseProvider(),
        HandlerProvider(),
        EmailMessageProvider(),
        HTTPProvider(),
    )
    setup_dishka(container, app)
    
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(app), host="127.0.0.1", port=8000)