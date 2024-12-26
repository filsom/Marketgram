from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
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
    USER_ID = UUID('61860a73-2d68-400d-8297-827bb1e14c70')
    SUPER_USER_ID = UUID('2140a32e-4df9-4105-8e8f-3d7c707efe5a')

    def test_taxable_amount_for_withdraw(self) -> None:
        # Arrange
        tax_payout = Decimal(0.1)
        amount_payout = Money(200)

        sut = self.make_payout(amount_payout, 0, False, False)
        sut.accept_agreement(self.provide_agreement(tax_payout))

        # Act
        result = sut.calculate()

        # Assert
        assert amount_payout - (amount_payout * tax_payout) == result
        assert len(sut.entries) == 2

    def make_payout(
        self, 
        tax_free: Money, 
        count_block: int, 
        is_processed: bool, 
        is_blocked: bool
    ) -> Payout:
        return Payout(
            self.USER_ID,
            'test_*',
            tax_free,
            datetime.now(),
            None,
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
                Operation.BUY, EntryStatus.FREEZ
            )
        )
        agreement.add_rule(
            EventType.TAX_PAYOUT, 
            PayoutTaxFormula(
                self.SUPER_USER_ID, 
                AccountType.TAX, 
                Operation.BUY, 
                EntryStatus.FREEZ
            )
        )
        return agreement