from contextlib import asynccontextmanager

from dishka import make_async_container
import uvicorn
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from marketgram.common.ioc import DatabaseProvider
from marketgram.identity.access.ioc import IdentityAccessIoC
# from marketgram.identity.access.port.adapter.fastapi_resources import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await app.state.dishka_container.close()

    
app = FastAPI(lifespan=lifespan)


def create_app(app):
    # container = make_async_container(
    #     DatabaseProvider(),
    #     IdentityAccessIoC(),
    # )
    # setup_dishka(container, app)
    
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(app), host="127.0.0.1", port=8000)