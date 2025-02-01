from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.cancellation_deal import (
    CancellationDeal
)
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.errors import (
    PAYMENT_TO_SELLER, 
    RETURN_TO_BUYER, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class TestCancellationDeal:
    @pytest.mark.parametrize(
        'status', [
            StatusDeal.NOT_SHIPPED,
            StatusDeal.INSPECTION,
            StatusDeal.DISPUTE,
        ]
    )
    def test_seller_cancels_the_deal(self, status) -> None:
        # Arrange
        deal = self.make_deal(status=status)

        # Act
        deal.cancel(datetime.now(UTC))

        # Assert
        assert deal.status == StatusDeal.CANCELLED
        assert len(deal.entries) == 1
        assert len(deal.events) == 1

    @pytest.mark.parametrize(
        'status, excvalue', [
            (StatusDeal.NOT_SHIPPED, RETURN_TO_BUYER),
            (StatusDeal.INSPECTION, PAYMENT_TO_SELLER)
        ]
    )
    def test_seller_cancels_deal_with_expired_deadlines(self, status, excvalue) -> None:
        # Act
        deal = self.make_deal(status=status)

        # Assert
        with pytest.raises(CheckDeadlineError) as excinfo:
            deal.cancel(datetime.now(UTC) + timedelta(hours=2))

        # Assert
        assert str(excinfo.value) == excvalue
        assert deal.status == status
        assert len(deal.entries) == 0
        assert len(deal.events) == 0

    def make_deal(self, status: StatusDeal) -> CancellationDeal:
        deadlines = ActionTime(1, 1).create_deadlines(datetime.now(UTC))
        return CancellationDeal(
            1, 
            uuid4(),
            Money(200),
            deadlines,
            status,
            []
        )