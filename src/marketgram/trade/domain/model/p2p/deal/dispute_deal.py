from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.trade_item1.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.rule.agreement.entry import PostingEntry
from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.p2p.payout import Payout
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class DisputeDeal:
    def __init__(
        self,
        deal_id: int,
        members: Members,
        price: Money,
        is_disputed: bool,
        deadlines: Deadlines,
        status: StatusDeal,
        deal_entries: list[PostingEntry] | None = None,
        payout: Payout | None = None
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._price = price
        self._deadlines = deadlines
        self._deal_entries = deal_entries
        self._status = status
        self._is_disputed = is_disputed
        self._payout = payout

    def open_dispute(self, occurred_at: datetime) -> None:   
        if self._is_disputed:
            raise DomainError()
        
        if self._deadlines.inspection < occurred_at:
            raise DomainError()
        
        if self._deal_entries is not None:
            self._edit_entries_statuses(
                EntryStatus.TIME_BLOCK
            )
        if self._payout is not None: 
            if self._payout.created_at < occurred_at:
                self._payout.temporarily_block()

        self._is_disputed = True
        self._status = StatusDeal.DISPUTE

    def satisfy_seller(self, occurred_at: datetime) -> None:
        if self._deal_entries is not None:
            self._edit_entries_statuses(
                EntryStatus.FREEZ
            )
        if self._payout is not None:
            if self._payout.created_at < occurred_at:
                self._payout.unlock()

        self._status = StatusDeal.CLOSED

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._deal_entries is not None:
            self._edit_entries_statuses(
                EntryStatus.CANCELLED
            )
        self._deal_entries.append(
            PostingEntry(
                self.buyer_id,
                self._price,
                datetime.now(),
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        if self._payout is not None: 
            if self._payout.created_at < occurred_at:
                self._payout.unlock()

        self._status = StatusDeal.CANCELLED  

    def add_payout(self, payout: Payout) -> None:
        self._payout = payout

    def _edit_entries_statuses(self, status: EntryStatus) -> None:
        for entry in self._deal_entries:
            entry.update_status(status)

    @property
    def seller_id(self) -> UUID:
        return self._members.seller_id
    
    @property
    def buyer_id(self) -> UUID:
        return self._members.buyer_id
    
    @property
    def is_disputed(self) -> bool:
        return self._is_disputed
    
    @property
    def status(self) -> StatusDeal:
        return self._status
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DisputeDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)