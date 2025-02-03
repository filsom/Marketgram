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
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.trade_item.service import Service
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory


USER_ID_1 = UUID('c1378012-31df-4b23-80d9-78d31c6999b7')
USER_ID_2 = UUID('49fde197-f018-428a-8566-bae6f5d07b99')
BUYER_ID = 1
SELLER_ID = 2
CATEGORY_ID = 1
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
        category = Category(
            SERVICE_ID, 
            TCATEGORY_ID, 
            'accounts-123456', 
            ActionTime(1, 1), 
            Shipment.HAND, 
            Money(100), 
            Decimal(0.1), 
            1
        )
        card = category.new_card(
            SELLER_ID,
            Description('Telegram Acc', 'New Acc', StatusDescription.CURRENT),
            Money('100'),
            {},
            ActionTime(1, 1),
            datetime.now(UTC)
        )
        session.add_all([user, seller, type_category, service, category, card])
        await session.commit()

    async with AsyncSession(engine) as session:
        await session.begin()
        


    yield

    async with AsyncSession(engine) as session:
        await session.begin()

        await session.commit()