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
from marketgram.trade.domain.model.types import INFINITY
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
from datetime import UTC, datetime
from decimal import Decimal
from typing import AsyncGenerator
from uuid import UUID
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.user import User
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.description import Description, StatusDescription
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard
from marketgram.trade.domain.model.trade_item.service import Service
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory


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


USER_ID_1 = UUID('c1378012-31df-4b23-80d9-78d31c6999b7')
USER_ID_2 = UUID('49fde197-f018-428a-8566-bae6f5d07b99')
BUYER_ID = 1
SELLER_ID = 2
CATEGORY_ID = 1
TCATEGORY_ID = 1
SERVICE_ID = 1
CARD_ID = 1
DESC_ID = 1


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        'postgresql+psycopg://postgres:som@localhost:5433',
        echo=False,
    )
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    # async with AsyncSession(engine) as session:
    #     await session.begin()
    #     user = User(USER_ID_1, member_id=BUYER_ID, entries=[])
    #     seller = User(USER_ID_2, member_id=SELLER_ID, entries=[])
    #     session.add_all([user, seller])
    #     await session.flush()

    #     type_category = TypeCategory('Accounts', TCATEGORY_ID)
    #     session.add(type_category)
    #     await session.flush()

    #     service = Service('Telegram', 'telegram-123456', [], SERVICE_ID)
    #     session.add(service)
    #     await session.flush()
    #     category = Category(
    #         SERVICE_ID, 
    #         TCATEGORY_ID, 
    #         'accounts-123456', 
    #         ActionTime(1, 1), 
    #         Shipment.HAND, 
    #         Money(100), 
    #         Decimal(0.1), 
    #         1
    #     )
    #     session.add(category)
    #     await session.flush()
    #     card = ModerationCard(
    #         SELLER_ID,
    #         CATEGORY_ID,
    #         Money(200),
    #         Money(200),
    #         [],
    #         {'spam_block': False},
    #         ActionTime(1, 1),
    #         Shipment.HAND,
    #         datetime.now(UTC),
    #         StatusCard.ON_SALE,
    #         CARD_ID
    #     )
    #     session.add(card)
    #     await session.flush()

    #     d = Description('Telegram Acc', 'New Acc', StatusDescription.CURRENT, set_in=datetime.now(UTC), card_id=CARD_ID)
    #     session.add(d)
        
    #     # session.add_all([user, seller, type_category, service, category, card])
    #     await session.commit()
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