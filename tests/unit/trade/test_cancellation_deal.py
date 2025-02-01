from datetime import UTC, datetime
from uuid import uuid4

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal


class TestCancellationDeal:
    def test_seller_cancelled_deal(self) -> None:
        # Arrange
        deal = CancellationDeal(
            1,
            uuid4(),
            Money(200),
            StatusDeal.NOT_SHIPPED,
            []
        )

        # Act
        deal.cancel(datetime.now(UTC))

        # Assert
        assert len(deal.events) == 1
        assert len(deal.entries) == 1
        assert deal.status == StatusDeal.CANCELLED