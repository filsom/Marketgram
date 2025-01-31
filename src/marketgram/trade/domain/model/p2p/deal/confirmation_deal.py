from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.sales_manager import ServiceAgreement
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.types import AccountType, Operation
    

class ConfirmationDeal:
    def __init__(
        self, 
        deal_id: int,
        seller_id: UUID,
        price: Money,
        deadlines: Deadlines,
        status: StatusDeal,
        inspected_at: datetime | None,
        entries: list[PostingEntry]
    ) -> None:
        self._deal_id = deal_id
        self._seller_id = seller_id
        self._price = price
        self._deadlines = deadlines
        self._status = status
        self._inspected_at = inspected_at
        self._entries = entries

    def confirm_quality(
        self, 
        occurred_at: datetime,
        agreement: ServiceAgreement
    ) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise DomainError()

        self._entries.append(
            PostingEntry(
                self._seller_id,
                agreement.calculate_payment_to_seller(self._price),
                occurred_at,
                AccountType.SELLER,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        self._entries.append(
            PostingEntry(
                agreement._manager_id,
                agreement.calculate_sales_profit(self._price),
                occurred_at,
                AccountType.TAX,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        self._inspected_at = occurred_at
        self._status = StatusDeal.CLOSED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfirmationDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)