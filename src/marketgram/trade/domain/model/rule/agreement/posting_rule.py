from marketgram.trade.domain.model.rule.agreement.entry import EntryStatus
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class PostingRule:
    def __init__(
        self,
        account_type: AccountType,
        operation_type: Operation,
        entry_status: EntryStatus
    ) -> None:
        self._account_type = account_type
        self._operation_type = operation_type
        self._entry_status = entry_status

    @property
    def account_type(self) -> AccountType:
        return self._account_type
    
    @property
    def operation_type(self) -> Operation:
        return self._operation_type
    
    @property   
    def entry_status(self) -> EntryStatus:
        return self._entry_status