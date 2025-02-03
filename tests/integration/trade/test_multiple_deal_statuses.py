from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.trade.port.adapter.sqlalchemy_resources.cards_repository import CardsRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
from tests.integration.trade.conftest import BUYER, SELLER, MANAGER, CARD_ID
from tests.integration.trade.trade_test_case import TradeTestCase


@pytest.mark.usefixtures('create_card')
class TestMultipleDealStatuses(TradeTestCase):
    async def test_create_new_deal(self) -> None:
        # Arrange
        async with AsyncSession(self._engine) as session:
            card = await CardsRepository(session).sell_card_with_id(CARD_ID)

        # Act
            deal = card.purchase(BUYER[1], 1, datetime.now(UTC))
            session.add(deal)
            await session.commit()

        # Assert
        deal = await self.query_multiple_deal_statuses()
        deal.can_be_shipped() \
            .cannot_be_confirmed() \
            .can_be_closed() \
            .cannot_open_duspute() \
            .there_was_no_dispute()

    async def test_seller_has_shipped_the_items(self) -> None:
        # Arrange
        async with AsyncSession(self._engine) as session:
            await session.begin()
            current_time = datetime.now(UTC)
            deal_id = await self.query_deal_id()
            deal = await DealsRepository(session).unshipped_with_id(SELLER[1], deal_id)
            deal.add_download_link('https://github.com/', current_time)

        # Act
            deal.confirm_shipment(current_time)
            await session.commit()

        # Assert
        deal = await self.query_multiple_deal_statuses()
        deal.cant_ship() \
            .can_be_сonfirmed() \
            .can_be_closed() \
            .can_open_dispute() \
            .there_was_no_dispute()

    async def test_buyer_confirms_the_quality_of_the_items(self) -> None:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            deal_id = await self.query_deal_id()
            deal = await DealsRepository(session).unconfirmed_with_id(BUYER[1], deal_id)

        # Act
            deal.confirm_quality(
                datetime.now(UTC),
                self.make_service_agreement()
            )
            await session.commit()

        # Assert
        deal = await self.query_multiple_deal_statuses()
        deal.cant_ship() \
            .cannot_be_confirmed() \
            .cant_be_closed() \
            .cannot_open_duspute() \
            .there_was_no_dispute()