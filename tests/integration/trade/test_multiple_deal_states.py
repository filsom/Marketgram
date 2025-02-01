from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard
from tests.integration.trade.trade_test_case import TradeTestCase


OWNER_ID = ...
BUYER_ID = ...
CARD_ID = ...



@pytest_asyncio.mark.usefixtures('create_card')
class TestMultipleDealStates(TradeTestCase):
    async def test_creating_new_deal(self):
        pass