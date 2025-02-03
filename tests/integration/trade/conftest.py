from datetime import UTC, datetime
from decimal import Decimal
from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy import UUID
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


BUYER_ID = 1
SELLER_ID = 2
MANAGER_ID = 3
CARD_ID = 1


async def create_card(engine: AsyncGenerator[AsyncEngine, None]) -> None:
    async with AsyncSession(engine) as session:
        await session.begin()
        for member_id in [BUYER_ID, SELLER_ID, MANAGER_ID]:
            user = User(uuid4(), member_id=member_id, entries=[])
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
            SELLER_ID,
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