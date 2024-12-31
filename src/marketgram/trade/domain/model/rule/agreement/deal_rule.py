from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.spa.confirmation_deal import (
    ConfirmationDeal
)
from marketgram.trade.domain.model.rule.agreement.limits import Limits
from marketgram.trade.domain.model.rule.agreement.posting_rule import (
    PostingRule
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    EventType, 
    Operation
)
from marketgram.trade.domain.model.rule.agreement.entry import (
    PostingEntry, 
    EntryStatus
)
from marketgram.trade.domain.model.rule.agreement.money import Money
    

class DealPostingRule(PostingRule):
    def make_entry(self, deal: ConfirmationDeal, amount: Money) -> None:
        entry = PostingEntry(
            deal._seller_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        deal.add_entry(entry)
    
    def process(self, deal: ConfirmationDeal, limits: Limits) -> None:
        self.make_entry(deal, self.calculate_amount(
            deal._price, limits
        ))

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        raise NotImplementedError
    

class PaymentFormula(DealPostingRule):
    def process(self, deal: ConfirmationDeal, limits: Limits) -> None:
        super().process(deal, limits)
        secondary_rule = deal.agreement.find_deal_rule(
            EventType.TAX_PAYMENT
        )
        secondary_rule.process(deal, limits)

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        return amount - amount * limits.tax_payment    


class PaymentTaxFormula(DealPostingRule):
    def __init__(
        self, 
        superuser_id: UUID,
        account_type: AccountType,
        operation_type: Operation,
        entry_status: EntryStatus
    ) -> None:
        super().__init__(
            account_type, 
            operation_type, 
            entry_status
        )
        self._superuser_id = superuser_id

    def make_entry(self, deal: ConfirmationDeal, amount: Money) -> None:
        entry = PostingEntry(
            self._superuser_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        deal.add_entry(entry)

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        return amount * limits.tax_payment