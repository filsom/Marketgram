from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import registry

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_identity_mapper import identity_registry_mapper
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_identity_table import (
    role_table, 
    user_table, 
    web_session_table
)


@pytest_asyncio.fixture(loop_scope='session')
async def sqlalchemy_async_engine():
    engine = create_async_engine(
        'postgresql+psycopg://postgres:som@localhost:5433',
        echo=False,
    )
    mapper = registry()
    identity_registry_mapper(mapper)
    
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(loop_scope='function')
async def async_session(
    sqlalchemy_async_engine: AsyncGenerator[AsyncEngine]
) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(sqlalchemy_async_engine) as session:
        yield session