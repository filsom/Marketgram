# from datetime import UTC, datetime

# from sqlalchemy.ext.asyncio import AsyncSession

# from marketgram.trade.domain.model.trade_item.sell_card import SellCard
# from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
# from tests.integration.trade.trade_test_case import TradeTestCase


# BUYER_ID = ...
# SELLER_ID = ...
# CARD_ID = ...


# class TestMultipleDealStatuses(TradeTestCase):
#     async def create_new_deal(self, card: SellCard) -> None:
#         # Arrange
#         new_deal = card.purchase(BUYER_ID, 1, datetime.now(UTC))

#         # Act
#         async with AsyncSession(self._engine) as session:
#             await session.begin()
#             await session.add(new_deal)
#             await session.commit()

#         # Arrange

#         async with AsyncSession(self._engine) as session:
#             deals_repository = DealsRepository(session)

#             unshipped_deal  = await deals_repository.unshipped_with_id(SELLER_ID, )
#             unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER_ID, ...)
#             unclosed_deal = await deals_repository.unclosed_with_id(SELLER_ID, ...)
#             not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER_ID, ...)
#             disputed_deal = await deals_repository.disputed_with_id(...)

#             assert unshipped_deal is not None
#             assert unconfirmed_deal is None
#             assert unclosed_deal is not None
#             assert not_disputed_deal is None
#             assert disputed_deal is None