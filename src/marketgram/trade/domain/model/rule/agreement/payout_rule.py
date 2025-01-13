from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

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

if TYPE_CHECKING:
    from marketgram.trade.domain.model.rule.agreement.service_agreement import (
        ServiceAgreement
    )


class PayoutPostingRule(PostingRule):
    def make_entry(
        self, 
        member_id: UUID, 
        empty_list: list, 
        amount: Money
    ) -> None:
        entry = PostingEntry(
            member_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        empty_list.append(entry)

    def process(
        self, 
        member_id: UUID,
        amount: Money,
        empty_list: list, 
        agreement: ServiceAgreement,
        occurred_at: datetime
    ) -> list[PostingEntry]:
        limits = agreement.limits_from(occurred_at)

        self.make_entry(
            member_id, 
            empty_list, 
            self.calculate_amount(amount, limits)
        )

        return empty_list

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        raise NotImplementedError


class PayoutFormula(PayoutPostingRule):
    def process(
        self, 
        member_id: UUID,
        amount: Money,
        empty_list: list, 
        agreement: ServiceAgreement,
        occurred_at: datetime
    ) -> list[PostingEntry]:
        super().process(
            member_id, 
            amount, 
            empty_list, 
            agreement, 
            occurred_at
        )
        secondary_rule = agreement.find_payout_rule(EventType.TAX_PAYOUT)
        secondary_rule.process(
            member_id, 
            amount, 
            empty_list, 
            agreement, 
            occurred_at
        )

        return empty_list
    
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

    def make_entry(
        self, 
        member_id: UUID, 
        empty_list: list, 
        amount: Money
    ) -> None:
        entry = PostingEntry(
            self._superuser_id,
            amount,
            datetime.now(),
            self._account_type,
            self._operation_type,
            self._entry_status
        )
        empty_list.append(entry)

    def calculate_amount(self, amount: Money, limits: Limits) -> Money:
        return amount * limits.tax_payout