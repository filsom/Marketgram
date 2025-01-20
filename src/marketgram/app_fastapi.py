from contextlib import asynccontextmanager
from enum import Enum, StrEnum, auto
from typing import Annotated, Optional, Union

from dishka import make_async_container
from pydantic import BaseModel, Field
import uvicorn
from fastapi import Depends, FastAPI, Path, Query, Request
from dishka.integrations.fastapi import setup_dishka

from marketgram.common.ioc import DatabaseProvider
from marketgram.identity.access.ioc import IdentityAccessIoC
# from marketgram.identity.access.port.adapter.fastapi_resources import router
from pydantic.json_schema import SkipJsonSchema

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await app.state.dishka_container.close()

    
app = FastAPI(lifespan=lifespan)

class Type(str, Enum):
    man = 'man'
    women = 'women'

class Req(BaseModel):
    type: Type = Type.man
    x: str | None


class Req2(BaseModel):
    type: Type = Type.women
    y: int
    x: str | None

@app.post('/test/{type}/')
async def test(type: Type, r: Optional[Req | Req2]):
    return 'Ok'


def create_app(app):
    # container = make_async_container(
    #     DatabaseProvider(),
    #     IdentityAccessIoC(),
    # )
    # setup_dishka(container, app)
    
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(app), host="127.0.0.1", port=8000)