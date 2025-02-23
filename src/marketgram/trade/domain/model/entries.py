from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.errors import DiscountPriceError
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
        

@dataclass
class InventoryEntry:
    qty: int
    posted_in: datetime
    operation: InventoryOperation


@dataclass(order=True)
class PriceEntry:
    start_qty: int
    unit_price: Money
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PriceEntry):
            return False
        
        return self.start_qty == value.start_qty