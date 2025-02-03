from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
from tests.integration.conftest import BUYER_ID, SELLER_ID
from tests.integration.trade.trade_test_case import TradeTestCase



class TestMultipleDealStatuses(TradeTestCase):
    async def test_create_new_deal(self) -> None:
        # Arrange
        # async with AsyncSession(self._engine) as session:
        #     card = select(SellCard).where(SellCard._card_id == 1)
        #     r = await session.execute(card)
        #     ca = r.scalar()

        #     deal = ca.purchase(BUYER_ID, 1, datetime.now(UTC))
        #     session.add(deal)
        #     await session.commit()

        # Arrange

        # async with AsyncSession(self._engine) as session:
        #     deals_repository = DealsRepository(session)

        #     deal = await deals_repository.unshipped_with_id(SELLER_ID, 2)
        #     unshipped_deal  = await deals_repository.unshipped_with_id(SELLER_ID, 2)
        #     unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER_ID, 2)
        #     unclosed_deal = await deals_repository.unclosed_with_id(SELLER_ID, 2)
        #     not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER_ID, 2)
        #     disputed_deal = await deals_repository.disputed_with_id(2)

        #     assert unshipped_deal is not None
        #     assert unconfirmed_deal is None
        #     assert unclosed_deal is not None
        #     assert not_disputed_deal is None
        #     assert disputed_deal is None
        pass

    async def test_shipped(self):
        async with AsyncSession(self._engine) as session:
            await session.begin()
            deals_repository = DealsRepository(session)
            
            deal = await deals_repository.unshipped_with_id(SELLER_ID, 2)
            deal.add_download_link('123123', datetime.now(UTC))
            deal.confirm_shipment(datetime.now(UTC))
            await session.commit()

        async with AsyncSession(self._engine) as session:
            deals_repository = DealsRepository(session)
            unshipped_deal  = await deals_repository.unshipped_with_id(SELLER_ID, 2)
            unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER_ID, 2)
            unclosed_deal = await deals_repository.unclosed_with_id(SELLER_ID, 2)
            not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER_ID, 2)
            disputed_deal = await deals_repository.disputed_with_id(2)

            assert unshipped_deal is None
            assert unconfirmed_deal is not None
            assert unclosed_deal is not None
            assert not_disputed_deal is not None
            assert disputed_deal is None

    async def test_shipped(self):
        async with AsyncSession(self._engine) as session:
            await session.begin()
            deals_repository = DealsRepository(session)
            
            deal = await deals_repository.unconfirmed_with_id(SELLER_ID, 2)
            deal.confirm_quality(datetime.now(UTC))
            await session.commit()

        async with AsyncSession(self._engine) as session:
            deals_repository = DealsRepository(session)
            unshipped_deal  = await deals_repository.unshipped_with_id(SELLER_ID, 2)
            unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER_ID, 2)
            unclosed_deal = await deals_repository.unclosed_with_id(SELLER_ID, 2)
            not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER_ID, 2)
            disputed_deal = await deals_repository.disputed_with_id(2)

            assert unshipped_deal is None
            assert unconfirmed_deal is not None
            assert unclosed_deal is not None
            assert not_disputed_deal is not None
            assert disputed_deal is None