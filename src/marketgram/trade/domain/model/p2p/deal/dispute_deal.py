from datetime import datetime

from marketgram.trade.domain.model.events import (
    DisputeClosedEvent, 
    DisputeOpenedEvent
)
from marketgram.trade.domain.model.p2p.errors import (
    DO_NOT_OPEN_DISPUTE, 
    REIPENING,
    DisputeError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import AccountType, Operation


class DisputeDeal:
    def __init__(
        self,
        deal_id: int,
        members: Members,
        price: Money,
        deadlines: Deadlines,
        status: StatusDeal,
        is_disputed: bool,
        entries: list[PostingEntry] | None,
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._price = price
        self._deadlines = deadlines
        self._entries = entries
        self._status = status
        self._is_disputed = is_disputed
        self.events = []

    def open_dispute(self, occurred_at: datetime) -> None:   
        if self._is_disputed:
            raise DisputeError(REIPENING)
        
        if self._deadlines.check(self._status, occurred_at):
            raise DisputeError(DO_NOT_OPEN_DISPUTE)

        self.events.append(
            DisputeOpenedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._is_disputed = True
        self._status = StatusDeal.DISPUTE

    def satisfy_seller(
        self, 
        occurred_at: datetime,
        agreement: ServiceAgreement
    ) -> None:
        self._entries.append(
            PostingEntry(
                self._members.seller_id,
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
                AccountType.MANAGER,
                Operation.SALE,
                EntryStatus.ACCEPTED
            )
        )
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CLOSED

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        self._entries.append(
            PostingEntry(
                self._members.buyer_id,
                self._price,
                datetime.now(),
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CANCELLED  
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DisputeDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)