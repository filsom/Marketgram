from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterable

from dishka import AsyncContainer
from fastapi import Request, Response


@asynccontextmanager
async def RequestContainer(
    request: Request, 
    response: Response
) -> AsyncGenerator[AsyncContainer]:
    async with request.app.state.dishka_container(
        context={
            Request: request, 
            Response: response
        }
    ) as container:
        yield container


@asynccontextmanager
async def Container(
    request: Request, 
) -> AsyncGenerator[AsyncContainer]:
    async with request.app.state.dishka_container() as container:
        yield container