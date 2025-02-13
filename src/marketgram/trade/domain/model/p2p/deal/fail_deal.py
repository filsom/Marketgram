from datetime import datetime

from marketgram.common.entity import Entity
from marketgram.trade.domain.model.notifications import SellerCancelledDealNotification
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.errors import (
    PAYMENT_TO_SELLER, 
    RETURN_TO_BUYER, 
    CheckDeadlineError,
)
from marketgram.trade.domain.model.entries import PostingEntry
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import EntryStatus, StatusDeal
from marketgram.trade.domain.model.types import AccountType, Operation


class FailDeal(Entity):
    def __init__(
        self,
        deal_id: int,
        buyer_id: int,
        unit_price: Money,
        qty_purchased: int,
        deadlines: Deadlines,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        super().__init__()
        self._deal_id = deal_id
        self._buyer_id = buyer_id
        self._unit_price = unit_price
        self._qty_purchased = qty_purchased
        self._deadlines = deadlines
        self._status = status
        self._entries = entries

    def cancel(self, occurred_at: datetime) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            match self._status:
                case StatusDeal.NOT_SHIPPED:
                    raise CheckDeadlineError(RETURN_TO_BUYER)
                
                case StatusDeal.INSPECTION:
                    raise CheckDeadlineError(PAYMENT_TO_SELLER)     

        self._entries.append(
            PostingEntry(
                self._buyer_id,
                self.amount_return,
                occurred_at,
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        self.add_event(
            SellerCancelledDealNotification(
                self._buyer_id,
                self._deal_id,
                occurred_at
            )
        )
        self._status = StatusDeal.CANCELLED
    
    @property
    def status(self) -> StatusDeal:
        return self._status
    
    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries

    @property
    def amount_return(self) -> Money:
        return self._qty_purchased * self._unit_price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FailDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)