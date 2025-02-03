from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine


class TradeTestCase:
    @pytest.fixture(autouse=True)
    def _set_async_engine(
        self, 
        engine: AsyncGenerator[AsyncEngine, None]
    ) -> None:
        self._engine = engine

    async def query_multiple_deal_statuses(seller_id, buyer_id, deal_id):
        pass