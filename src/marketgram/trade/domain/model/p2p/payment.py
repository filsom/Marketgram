from datetime import datetime
from uuid import UUID

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.entries import (
    EntryStatus, 
    PostingEntry
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import (
    AccountType, 
    Operation
)


class Payment:
    def __init__(
        self,
        payment_id: UUID,
        user_id: UUID,
        amount: Money,
        created_at: datetime,
        is_processed: bool = False,
        is_blocked: bool = False,
    ) -> None:
        self._payment_id = payment_id
        self._user_id = user_id
        self._amount = amount
        self._created_at = created_at
        self._is_processed = is_processed
        self._is_blocked = is_blocked
        self._entries: list[PostingEntry] = []

    def accept(self) -> None:
        if self._is_blocked or self._is_processed:
            raise DomainError()
            
        new_entry = PostingEntry(
            self._user_id,
            self._amount,
            self._created_at,
            AccountType.USER,
            Operation.PAYMENT,
            EntryStatus.ACCEPTED
        )
        self._is_processed = True

        self._entries.append(new_entry)

    def __eq__(self, other: 'Payment') -> bool:
        if not isinstance(other, Payment):
            return False

        return self._payment_id == other._payment_id
    
    def __hash__(self) -> int:
        return hash(self._payment_id)