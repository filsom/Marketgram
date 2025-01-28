from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item1.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.rule.agreement.entry import PostingEntry
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation
    

class ConfirmationDeal:
    def __init__(
        self, 
        deal_id: int,
        seller_id: UUID,
        price: Money,
        sales_tax: Decimal,
        card_created_at: datetime,
        deadlines: Deadlines,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        self._deal_id = deal_id
        self._seller_id = seller_id
        self._price = price
        self._sales_tax = sales_tax
        self._card_created_at = card_created_at
        self._deadlines = deadlines
        self._status = status
        self._entries = entries

    def confirm_quality(
        self, 
        superuser_id: UUID, 
        occurred_at: datetime
    ) -> None:
        if self._deadlines.inspection < occurred_at:
            raise DomainError()

        self._entries.append(
            PostingEntry(
                self._seller_id,
                self._price - self._price * self._sales_tax,
                occurred_at,
                AccountType.SELLER,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        self._entries.append(
            PostingEntry(
                superuser_id,
                self._price * self._sales_tax,
                occurred_at,
                AccountType.TAX,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        self._status = StatusDeal.CLOSED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfirmationDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)