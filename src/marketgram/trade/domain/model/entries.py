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


@dataclass
class PriceEntry:
    start_qty: int
    unit_price: Money
    discount: list[Decimal] = field(default_factory=list)

    def set_discount(
        self,
        new_price: Money, 
        minimum_price: Money, 
        minimum_procent_discount: Decimal
    ) -> None:
        if len(self.discount):
            raise DiscountPriceError()
        
        if new_price < minimum_price or new_price >= self.unit_price:
            raise DiscountPriceError()
        
        discount_procent = 100 - new_price._value / self.unit_price._value * 100
        if discount_procent < minimum_procent_discount:
            raise DiscountPriceError()
        
        self.discount.append(discount_procent)

    def remove_discount(self) -> None:
        self.discount.clear()    