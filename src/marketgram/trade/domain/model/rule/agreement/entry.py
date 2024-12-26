from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class Entry:
    def __init__(
        self,
        user_id: UUID,
        amount: Money,
        posted_in: datetime,
        account_type: AccountType,
        operation: Operation,
        entry_status: EntryStatus
    ) -> None:
        self._user_id = user_id
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

    def __repr__(self) -> str:
        return (
            f'PostingEntry('
                f'user_id={self._user_id}, '
                f'amount={self._amount}, ' 
                f'posted_in={self._posted_in}, ' 
                f'account_type={self._account_type}, ' 
                f'operation={self._operation}, ' 
                f'entry_status={self._entry_status}, ' 
                f'is_archived={self._is_archived}' 
            ')'
        )