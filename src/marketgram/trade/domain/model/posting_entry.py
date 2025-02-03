from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import AccountType, Operation


class PostingEntry:
    def __init__(
        self,
        member_id: int,
        amount: Money,
        posted_in: datetime,
        account_type: AccountType,
        operation: Operation,
        entry_status: EntryStatus
    ) -> None:
        self._member_id = member_id
        self._amount = amount
        self._account_type = account_type
        self._operation = operation
        self._posted_in = posted_in
        self._entry_status = entry_status 
        self._is_archived = False       

    def update_status(self, status: EntryStatus) -> None:
        self._entry_status = status

    def time_adjustment(self, occurr_at: datetime) -> None:
        self._posted_in = occurr_at

    def archive(self) -> None:
        self._is_archived = True