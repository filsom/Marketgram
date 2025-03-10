import os
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import registry

from marketgram.common.sqlalchemy_metadata import metadata
from marketgram.identity.access.port.adapter import (
    users_registry_mapper,
    roles_registry_mapper,
    web_sessions_registry_mapper,
    user_table,
    role_table,
    web_session_table,    
)


mapper = registry()
users_registry_mapper(mapper)
web_sessions_registry_mapper(mapper)
roles_registry_mapper(mapper)


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        os.getenv('DB_URL'),
        echo=False,
    )
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
    
    await engine.dispose()