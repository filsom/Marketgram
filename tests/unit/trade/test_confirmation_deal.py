from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class TestConfirmationDeal:
    def test_buyer_confirms_the_quality_of_the_items(self) -> None:
        # Arrange
        occurred_at = datetime.now(UTC)
        service_agreement = self.make_service_agreement()
        deal = self.make_deal(occurred_at)

        # Act
        deal.confirm_quality(occurred_at, service_agreement)

        # Assert
        assert deal.status == StatusDeal.CLOSED
        assert deal.inspected_at == occurred_at
        assert len(deal.entries) == 2

    def make_deal(self, created_at: datetime) -> ConfirmationDeal:
        deadlines = ActionTime(1, 1).create_deadlines(created_at)
        return ConfirmationDeal(
            1,
            uuid4(),
            Money(200),
            deadlines,
            StatusDeal.INSPECTION,
            None,
            []
        )
    
    def make_service_agreement(self) -> ServiceAgreement:
        return ServiceAgreement(
            uuid4(),
            Decimal('0.1'),
            Decimal('0.1'),
            Money(100),
            Money(100),
            datetime.now(UTC),
            agreement_id=1
        )