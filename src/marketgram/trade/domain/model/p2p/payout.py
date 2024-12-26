from __future__ import annotations
from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.rule.agreement.entry import (
    Entry
)
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.service_agreement import (
    ServiceAgreement
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    EventType
)


class Payout:
    def __init__(
        self,
        payout_id: UUID,
        user_id: UUID,
        paycard_synonym: str,
        tax_free: Money,
        created_at: datetime,
    ) -> None:
        self._payout_id = payout_id
        self._user_id = user_id
        self._paycard_synonym = paycard_synonym
        self._tax_free = tax_free
        self._created_at = created_at
        self._count_block = 0
        self._is_processed = False
        self._is_blocked = False
        self._agreement: ServiceAgreement = None
        self._entries: list[Entry] = []

    def undo(self) -> None:
        if self._is_processed:
            raise DomainError()
        
        self._is_processed = True

    def calculate_for_payout(self) -> Money:
        if self._is_processed or self._count_block:
            raise DomainError()
        
        self._collect_tax()

        for entry in self._entries:
            if entry._account_type == AccountType.SELLER:
                amount_payout = entry._amount

        self._is_processed = True

        return abs(amount_payout)

    def accept_agreement(self, agreement: ServiceAgreement) -> None:
        self._agreement = agreement

    def transferred_agreement(self) -> ServiceAgreement:
        return self._agreement

    def temporarily_block(self) -> None:
        if not self._is_blocked and not self._count_block:
            self._is_blocked = True

        self._count_block += 1

    def unlock(self) -> None:
        self._count_block -= 1

        if self._count_block == 0:
            self._is_blocked = False

    def provide_entries(self) -> list[Entry]:
        return self._entries

    def add_entry(self, entry) -> None:
        self._entries.append(entry) 

    def _collect_tax(self) -> None:
        limits = self._agreement.limits_from(self._created_at)

        rule = self._agreement.find_payout_rule(
            EventType.USER_DEDUCED
        )
        rule.process(self, limits)

    def __eq__(self, other: 'Payout') -> bool:
        if not isinstance(other, Payout):
            return False

        return self._payout_id == other._payout_id
    
    def __hash__(self) -> int:
        return hash(self._payout_id)