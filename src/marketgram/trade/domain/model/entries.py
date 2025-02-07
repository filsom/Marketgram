from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import EntryStatus
from marketgram.trade.domain.model.types import (
    AccountType, 
    InventoryOperation, 
    Operation  
)


@dataclass
class PostingEntry:
    user_id: UUID
    amount: Money
    posted_in: datetime
    account_type: AccountType
    operation: Operation
    entry_status: EntryStatus
        

@dataclass(frozen=True)
class InventoryEntry:
    qty: int
    posted_in: datetime
    operation: InventoryOperation