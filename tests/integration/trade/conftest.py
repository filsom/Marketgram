from datetime import UTC, datetime
from decimal import Decimal
from typing import AsyncGenerator
from uuid import UUID

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.user import User
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.description import Description
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard
from marketgram.trade.domain.model.trade_item.service import Service
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory


CARD_ID = 1
BUYER = (UUID('eb2eae40-c339-4228-a4ac-0c3b255fb2c8'), 1)
SELLER = (UUID('a49b67f2-92bd-4331-a0a4-31eba7db9b09'), 2)
MANAGER = (UUID('839e9ee0-2fa3-4e2a-8053-a03d95506852'), 3)


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def create_card(engine: AsyncGenerator[AsyncEngine, None]) -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        await session.begin()
        for identity in [BUYER, SELLER, MANAGER]:
            user = User(user_id=identity[0], member_id=identity[1], entries=[])
            session.add(user)

        type_category = TypeCategory('Accounts')
        session.add(type_category)
        await session.flush()

        service = Service('Telegram', 'telegram-123456', [])
        session.add(service)
        await session.flush()

        category = Category(
            service.service_id, 
            type_category.type_category_id, 
            'accounts-123456', 
            ActionTime(1, 1), 
            Shipment.HAND, 
            Money(100), 
            Decimal(0.1), 
        )
        session.add(category)            
        await session.flush()

        card = ModerationCard(
            SELLER[0],
            category.category_id,
            Money(200),
            Money(200),
            [],
            {'spam_block': False},
            ActionTime(1, 1),
            Shipment.HAND,
            datetime.now(UTC),
            StatusCard.ON_SALE,
            CARD_ID
        )
        session.add(card)
        await session.flush()

        description = Description(
            'Telegram Account', 
            'New Account TDATA/SESSION+JSON', 
            card_id=card.card_id
        )
        card.add_desciption(description)

        await session.commit()