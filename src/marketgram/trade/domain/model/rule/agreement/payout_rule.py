from __future__ import annotations
from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p_2.seller import Seller
from marketgram.trade.domain.model.rule.agreement.entry import (
    EntryStatus, 
    PostingEntry
)
from marketgram.trade.domain.model.rule.agreement.limits import Limits
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.posting_rule import (
    PostingRule
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    EventType, 
    Operation
)
from marketgram.trade.domain.model.p2p.payout import Payout


class PayoutPostingRule(PostingRule):
    def make_entry(self, payout: Payout, amount: Money) -> None:
        entry = PostingEntry(
            payout._user_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        payout.add_entry(entry)
    
    def process(self, seller: Seller, payout: Payout, limits: Limits) -> None:
        self.make_entry(payout, self.calculate_amount(
            payout._tax_free, limits
        ))

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        raise NotImplementedError


class PayoutFormula(PayoutPostingRule):
    def process(self, seller: Seller, payout: Payout, limits: Limits) -> None:
        super().process(seller, payout, limits)
        secondary_rule = seller._agreement.find_payout_rule(
            EventType.TAX_PAYOUT
        )
        secondary_rule.process(seller, payout, limits)

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        return -amount + amount * limits.tax_payout
    

class PayoutTaxFormula(PayoutPostingRule):
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

    def make_entry(self, payout: Payout, amount: Money) -> None:
        entry = PostingEntry(
            self._superuser_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        payout.add_entry(entry)

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        return amount * limits.tax_payout