from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.deal.events import (
    DisputeClosedEvent, 
    DisputeOpenedEvent
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.entry import PostingEntry
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
        deal_entries: list[PostingEntry] | None,
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._price = price
        self._deadlines = deadlines
        self._deal_entries = deal_entries
        self._status = status
        self._is_disputed = is_disputed
        self.events = []

    def open_dispute(self, occurred_at: datetime) -> None:   
        if self._is_disputed:
            raise DomainError()
        
        if self._deadlines.check(self._status, occurred_at):
            raise DomainError()
        
        if self._deal_entries is not None:
             for entry in self._deal_entries:
                 entry.update_status(EntryStatus.TIME_BLOCK)

        self.events.append(
            DisputeOpenedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._is_disputed = True
        self._status = StatusDeal.DISPUTE

    def satisfy_seller(self, occurred_at: datetime) -> None:
        if self._deal_entries is not None:
             for entry in self._deal_entries:
                 entry.update_status(EntryStatus.FREEZ)

        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CLOSED

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._deal_entries is not None:
             for entry in self._deal_entries:
                 entry.update_status(EntryStatus.CANCELLED)

        self._deal_entries.append(
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