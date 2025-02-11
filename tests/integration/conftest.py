from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import registry

from marketgram.identity.access.port.adapter.html_renderer import MessageRenderer
from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.identity.access.port.adapter.html_renderers import JwtTokenHtmlRenderer
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.users_registry import (
    users_registry_mapper
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.web_sessions_registry import (
    web_sessions_registry_mapper
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.roles_registry import (
    roles_registry_mapper
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.roles_table import (
    role_table
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.web_sessions_table import (
    web_session_table
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.users_table import (
    user_table
)
from marketgram.identity.access.settings import (
    Settings, 
    identity_access_load_settings
)



mapper = registry()
users_registry_mapper(mapper)
web_sessions_registry_mapper(mapper)
roles_registry_mapper(mapper)


@pytest.fixture(scope='session')
def settings() -> Settings:
    return identity_access_load_settings()


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        'postgresql+psycopg://postgres:som@localhost:5433',
        echo=False,
    )
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def activate_msg_renderer(
    settings: Settings
) -> MessageRenderer[str]:
    return JwtTokenHtmlRenderer(
        settings.jinja_env, 
        settings.activate_html_settings
    )


@pytest_asyncio.fixture(scope='function')
async def forgot_password_msg_renderer(
    settings: Settings
) -> MessageRenderer[str]:
    return JwtTokenHtmlRenderer(
        settings.jinja_env, 
        settings.forgot_pwd_html_settings
    )