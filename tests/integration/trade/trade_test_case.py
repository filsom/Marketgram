# from typing import AsyncGenerator

# import pytest
# from sqlalchemy.ext.asyncio import AsyncEngine


# class TradeTestCase:
#     @pytest.fixture(autouse=True)
#     def _set_async_engine(
#         self, 
#         engine: AsyncGenerator[AsyncEngine, None]
#     ) -> None:
#         self._engine = engine

#     async def query_multiple_deal_statuses(seller_id, buyer_id, deal_id):
#         unshipped_deal  = await deals_repository.unshipped_with_id(SELLER_ID, )
#         unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER_ID, ...)
#         unclosed_deal = await deals_repository.unclosed_with_id(SELLER_ID, ...)
#         not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER_ID, ...)
#         disputed_deal = await deals_repository.disputed_with_id(...)