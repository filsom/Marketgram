from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)


def create_app(app):
    container = ...
    setup_dishka(container, app)
    
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(app), host="127.0.0.1", port=8000)