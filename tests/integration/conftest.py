from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import registry

from marketgram.common.application.message_renderer import MessageRenderer
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
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.cards_registry import cards_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.cards_table import (
    cards_table,
    cards_descriptions_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.categories_registry import categories_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.categories_table import (
    categories_table,
    category_types_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_registry import deals_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table,
    deals_entries_table,
    deals_members_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.entries_registry import entries_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.entries_table import (
    entries_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.inventory_entries_registry import inventory_entries_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.inventory_entries_table import (
    inventory_entries_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.members_registry import members_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.members_table import (
    members_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.operations_registry import operations_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.operations_table import (
    operations_table,
    operations_entries_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.service_agreements_registry import service_agreements_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.service_agreements_table import (
    service_agreements_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.services_registry import services_registry_mapper
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.services_table import (
    services_table
)



mapper = registry()
users_registry_mapper(mapper)
web_sessions_registry_mapper(mapper)
roles_registry_mapper(mapper)
cards_registry_mapper(mapper)
categories_registry_mapper(mapper)
deals_registry_mapper(mapper)
entries_registry_mapper(mapper)
inventory_entries_registry_mapper(mapper)
members_registry_mapper(mapper)
operations_registry_mapper(mapper)
service_agreements_registry_mapper(mapper)
services_registry_mapper(mapper)

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