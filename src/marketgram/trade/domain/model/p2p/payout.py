from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.entry import PostingEntry
from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import AccountType, Operation


class Payout:
    def __init__(
        self,
        payout_id: UUID,
        user_id: UUID,
        paycard_synonym: str,
        tax_free: Money,
        created_at: datetime,
        entries: list[PostingEntry],
        count_block: int = 0,
        is_processed: bool = False,
        is_blocked: bool = False
    ) -> None:
        self._payout_id = payout_id
        self._user_id = user_id
        self._paycard_synonym = paycard_synonym
        self._tax_free = tax_free
        self._created_at = created_at
        self._count_block = count_block
        self._is_processed = is_processed
        self._is_blocked = is_blocked
        self._entries = entries

    def calculate(self, superuser_id: UUID, current_time: datetime) -> Money:
        if self._is_processed or self._count_block:
            raise DomainError()
        
        self._entries.append(
            PostingEntry(
                self._user_id,
                -self._tax_free + self._tax_free * Decimal('0.2'),
                current_time,
                AccountType.SELLER,
                Operation.PAYOUT,
                EntryStatus.ACCEPTED
            )
        )
        self._entries.append(
            PostingEntry(
                superuser_id,
                self._tax_free * Decimal('0.2'),
                current_time,
                AccountType.TAX,
                Operation.PAYMENT,
                EntryStatus.ACCEPTED
            )
        )
        for entry in self._entries:
            if entry._account_type == AccountType.SELLER:
                amount_payout = entry._amount

        self._is_processed = True

        return abs(amount_payout)
    
    def undo(self) -> None:
        if self._is_processed:
            raise DomainError()
        
        self._is_processed = True

    def temporarily_block(self) -> None:
        if not self._is_blocked and not self._count_block:
            self._is_blocked = True

        self._count_block += 1

    def unlock(self) -> None:
        self._count_block -= 1

        if self._count_block == 0:
            self._is_blocked = False

    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries
    
    @property
    def is_processed(self) -> bool:
        return self._is_processed
    
    @property
    def is_blocked(self) -> bool:
        return self._is_blocked
    
    @property
    def count_block(self) -> int:
        return self._count_block
    
    @property
    def created_at(self) -> datetime:
        return self._created_at

    def __eq__(self, other: 'Payout') -> bool:
        if not isinstance(other, Payout):
            return False

        return self._payout_id == other._payout_id
    
    def __hash__(self) -> int:
        return hash(self._payout_id)