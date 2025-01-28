from contextlib import asynccontextmanager
from decimal import Decimal
from enum import Enum, StrEnum, auto
from typing import Annotated, Any, List, Literal, Optional, Union

from dishka import make_async_container
from pydantic import BaseModel, Field, validator
import uvicorn
from fastapi import Body, Depends, FastAPI, Path, Query, Request
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

class X(BaseModel):
    g: int


class CreateCardRequest(BaseModel):
    service_id: int
    category_id: int
    price: Decimal
    title: Optional[str] = None
    body: str
    transfer_format: str
    x: list[X]


class CreateCard2Request(BaseModel):
    service_id: int
    category_id: int
    price: Decimal
    title: str
    body: str
    transfer_format: str

shemas = {
    1: CreateCardRequest,
    2: CreateCard2Request
}


@app.post("/create_card/")
async def create_item(
    # metadata: CreateCardRequest
    metadata: Any = Body(...)
):
    shema = shemas.get(metadata.get('service_id'))
    d = shema.model_validate(metadata).model_dump()
    print(d.get('x'))
    return d


def create_app(app):
    # container = make_async_container(
    #     DatabaseProvider(),
    #     IdentityAccessIoC(),
    # )
    # setup_dishka(container, app)
    
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(app), host="127.0.0.1", port=8000)