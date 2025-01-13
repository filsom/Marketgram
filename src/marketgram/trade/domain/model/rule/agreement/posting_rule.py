from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from marketgram.trade.domain.model.rule.agreement.entry import EntryStatus, PostingEntry
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation

if TYPE_CHECKING:
    from marketgram.trade.domain.model.rule.agreement.service_agreement import (
        ServiceAgreement
    )


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
        
    def process(
        self,
        member_id: UUID,
        amount: Money,
        empty_list: list, 
        agreement: ServiceAgreement,
        occurred_at: datetime
    ) -> list[PostingEntry]:
        raise NotImplementedError