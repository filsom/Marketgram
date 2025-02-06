from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.errors import (
    DO_NOT_OPEN_DISPUTE, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class TestDisputeDeal:
    def test_buyer_opened_a_dispute(self) -> None:
        # Arrange
        deal = self.make_deal(StatusDeal.INSPECTION)

        # Act
        deal.open_dispute(datetime.now(UTC))

        # Assert
        assert deal.status == StatusDeal.DISPUTE
        assert len(deal.events) == 1

    def test_buyer_did_not_have_time_to_open_a_dispute(self) -> None:
        # Arrange
        deal = self.make_deal(StatusDeal.INSPECTION)

        # Act
        with pytest.raises(CheckDeadlineError) as excinfo:
            deal.open_dispute(datetime.now(UTC) + timedelta(hours=2))

        # Assert
        assert str(excinfo.value) == DO_NOT_OPEN_DISPUTE
        assert deal.status == StatusDeal.INSPECTION
        assert len(deal.events) == 0

    def test_dispute_closed_in_favor_of_the_buyer(self) -> None:
        # Arrange
        deal = self.make_deal(StatusDeal.DISPUTE)

        # Act
        deal.satisfy_buyer(datetime.now(UTC))

        # Assert
        assert deal.status == StatusDeal.CANCELLED
        assert len(deal.events) == 1
        assert len(deal.entries) == 1

    def test_dispute_closed_in_favor_of_the_seller(self) -> None:
        # Arrange
        deal = self.make_deal(StatusDeal.DISPUTE)
        service_agreement = self.make_service_agreement()

        # Act
        deal.close_and_pay_the_seller(datetime.now(UTC), service_agreement)

        # Assert
        assert deal.status == StatusDeal.CLOSED
        assert len(deal.events) == 1
        assert len(deal.entries) == 2

    def make_deal(self, status: StatusDeal) -> DisputeDeal:
        deadlines = ActionTime(1, 1).create_deadlines(datetime.now(UTC))
        return DisputeDeal(
            1,
            Members(uuid4(), uuid4()),
            Money(200),
            deadlines,
            status,
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