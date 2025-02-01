from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4
import pytest

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.overdue_deal import OverdueDeal
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement


class TestOverdueDeal:
    @pytest.mark.parametrize(
        'status', [StatusDeal.NOT_SHIPPED, StatusDeal.INSPECTION]
    )
    def test_admin_closes_expired_deal(self, status) -> None:
        # Arrange
        deal = OverdueDeal(
            1, 
            Members(uuid4(), uuid4()),
            Money(200),
            status,
            []
        )
        service_agreement = ServiceAgreement(
            uuid4(),
            Decimal('0.1'),
            Decimal('0.1'),
            Money(100),
            Money(100),
            datetime.now(UTC),
            agreement_id=1
        )

        # Act
        deal.cancel(datetime.now(UTC), service_agreement)

        # Assert
        assert deal.status == StatusDeal.ADMIN_CLOSED