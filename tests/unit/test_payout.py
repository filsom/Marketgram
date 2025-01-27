from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.trade_item1.exceptions import DomainError
from marketgram.trade.domain.model.p2p.payout import Payout
from marketgram.trade.domain.model.rule.agreement.entry_status import (
    EntryStatus
)
from marketgram.trade.domain.model.rule.agreement.limits import Limits
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.payout_rule import (
    PayoutFormula, 
    PayoutTaxFormula
)
from marketgram.trade.domain.model.rule.agreement.service_agreement import (
    ServiceAgreement
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    EventType, 
    Operation
)


class TestPayuot:
    def test_blocking_a_previously_created_payout(self) -> None:
        # Arrange
        created_at = datetime.now(UTC) - timedelta(days=1)
        sut = self.make_payout(Money(100), created_at=created_at)

        dispute_deal = self.next_dispute_deal()
        dispute_deal.add_payout(sut)

        # Act
        dispute_deal.open_dispute(datetime.now(UTC))

        # Assert
        assert sut.count_block == 1
        assert sut.is_blocked == True
        assert sut.is_processed == False

    def test_blocking_future_payout(self) -> None:
        # Arrange
        created_at = datetime.now(UTC) + timedelta(days=1)
        sut = self.make_payout(Money(100), created_at=created_at)

        dispute_deal = self.next_dispute_deal()
        dispute_deal.add_payout(sut)

        # Act
        dispute_deal.open_dispute(datetime.now(UTC))

        # Assert
        assert sut.count_block == 0
        assert sut.is_blocked == False
        assert sut.is_processed == False

    def test_taxable_amount_for_withdraw(self) -> None:
        # Arrange
        tax_payout = Decimal(0.1)
        amount_payout = Money(200)

        sut = self.make_payout(amount_payout)
        sut.accept_agreement(self.provide_agreement(tax_payout))

        # Act
        result = sut.calculate()

        # Assert
        assert amount_payout - (amount_payout * tax_payout) == result
        assert len(sut.entries) == 2

    def test_cancellation_of_payout(self) -> None:
        # Arrange
        sut = self.make_payout(Money(200))

        # Act
        sut.undo()

        # Assert
        assert len(sut.entries) == 0
        assert sut.is_processed == True

    def test_blocking_payout_during_the_disputes(self) -> None:
        # Arrange
        sut = self.make_payout(Money(200))
        
        # Act
        sut.temporarily_block()
        sut.temporarily_block()

        # Assert
        assert sut.is_processed == False
        assert sut.is_blocked == True
        assert sut.count_block == 2

    def test_unblocking_payout_upon_completion_of_the_disputes(self) -> None:
        # Arrange
        sut = self.make_payout(Money(200))
        sut.temporarily_block()
        sut.temporarily_block() 

        # Act
        sut.unlock()
        sut.unlock()

        # Assert
        assert sut.is_processed == False
        assert sut.is_blocked == False
        assert sut.count_block == 0

    def test_calculation_of_payout_during_a_dispute(self) -> None:
        # Arrange
        sut = self.make_payout(Money(200))
        sut.temporarily_block()
        sut.temporarily_block() 
        sut.unlock()

        # Act
        with pytest.raises(DomainError) as excinfo:
            sut.calculate()        

        # Assert
        assert sut.is_processed == False
        assert sut.is_blocked == True
        assert sut.count_block == 1

    def next_dispute_deal(self) -> DisputeDeal:
        return DisputeDeal(
            1,
            Members(uuid4(), uuid4()),
            Money(200),
            False,
            TimeTags(
                datetime.now(UTC) - timedelta(hours=24),
                datetime.now(UTC) - timedelta(hours=12),
                datetime.now(UTC)
            ),
            Deadlines(1, 1, 1),
            StatusDeal.CHECK,
        )

    def make_payout(
        self, 
        tax_free: Money, 
        count_block: int = 0, 
        is_processed: bool = False, 
        is_blocked: bool = False,
        created_at: datetime = None
    ) -> Payout:
        if created_at is None:
            created_at = datetime.now(UTC)

        return Payout(
            uuid4(),
            uuid4(),
            'test_*',
            tax_free,
            created_at,
            count_block,
            is_processed,
            is_blocked
        )
    
    def provide_agreement(self, tax_payout: Decimal) -> ServiceAgreement:
        agreement = ServiceAgreement(uuid4())
        agreement.new_limits(
            Limits(
                Money(100), 
                Money(100), 
                Money(100), 
                Decimal(0.1), 
                Decimal(0.1), 
                tax_payout, 
                datetime.now()
            )
        )
        agreement.add_rule(
            EventType.USER_DEDUCED, 
            PayoutFormula(
                AccountType.SELLER, 
                Operation.BUY, EntryStatus.ACCEPTED
            )
        )
        agreement.add_rule(
            EventType.TAX_PAYOUT, 
            PayoutTaxFormula(
                uuid4(), 
                AccountType.TAX, 
                Operation.BUY, 
                EntryStatus.ACCEPTED
            )
        )
        return agreement