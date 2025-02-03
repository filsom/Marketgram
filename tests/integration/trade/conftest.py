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
from marketgram.trade.domain.model.trade_item.description import Description, StatusDescription
from marketgram.trade.domain.model.trade_item.service import Service
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory


USER_ID_1 = UUID('c1378012-31df-4b23-80d9-78d31c6999b7')
USER_ID_2 = UUID('49fde197-f018-428a-8566-bae6f5d07b99')
BUYER_ID = 1
SELLER_ID = 2
TCATEGORY_ID = 1
SERVICE_ID = 1


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def card(engine: AsyncGenerator[AsyncEngine, None]):
    async with AsyncSession(engine) as session:
        await session.begin()
        user = User(USER_ID_1, member_id=BUYER_ID)
        seller = User(USER_ID_2, member_id=SELLER_ID)

        type_category = TypeCategory('Accounts', TCATEGORY_ID)

        service = Service('Telegram', 'telegram-123456', [], SERVICE_ID)
        service.create_new_category(
            type_category,
            StatusDeal.NOT_SHIPPED,
            Shipment.HAND,
            ActionTime(1, 1),
            Money(50),
            Decimal('0.1')
        )
        card = service.categories[0].new_card(
            SELLER_ID,
            Description('Telegram Acc', 'New Acc', StatusDescription.CURRENT),
            Money('100'),
            {},
            ActionTime(1, 1),
            datetime.now(UTC)
        )
        session.add_all([user, seller, type_category, service, card])
        await session.commit()

    yield

    async with AsyncSession(engine) as session:
        await session.begin()

        await session.commit()