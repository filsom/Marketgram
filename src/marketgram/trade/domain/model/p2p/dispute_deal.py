from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.rule.agreement.entry import Entry
from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.p2p.payout import Payout
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class DisputeDeal:
    def __init__(
        self,
        deal_id: UUID,
        buyer_id: UUID,
        seller_id: UUID,
        price: Money,
        is_disputed: bool,
        time_tags: TimeTags,
        deadlines: Deadlines,
        deal_entries: list[Entry],
        status: StatusDeal,
        payout: Payout | None
    ) -> None:
        self._deal_id = deal_id
        self._buyer_id = buyer_id
        self._seller_id = seller_id
        self._price = price
        self._time_tags = time_tags
        self._deadlines = deadlines
        self._deal_entries = deal_entries
        self._status = status
        self._is_disputed = is_disputed
        self._payout = payout

    def open_dispute(self, occurred_at: datetime) -> None:   
        if self._is_disputed:
            raise DomainError()
            
        if self.dispute_deadline() < occurred_at:
            raise DomainError()
         
        if self._deal_entries:
            self._edit_entries_statuses(
                EntryStatus.TIME_BLOCK
            )
        if self._payout is not None:
            self._payout.temporarily_block()

        self._time_tags.closing_reset()
        self._is_disputed = True
        self._status = StatusDeal.DISPUTE

    def dispute_deadline(self) -> datetime:
        return (self._time_tags.received_at 
                + self._deadlines.total_check_hours)

    def satisfy_seller(self, occurred_at: datetime) -> None:
        if self._deal_entries:
            self._edit_entries_statuses(
                EntryStatus.FREEZ
            )
        if self._payout is not None:
            self._payout.unlock()

        self._time_tags.closed(occurred_at)
        self._status = StatusDeal.CLOSED

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._deal_entries:
            self._edit_entries_statuses(
                EntryStatus.CANCELLED
            )
        self._deal_entries.append(
            Entry(
                self._buyer_id,
                self._price,
                datetime.now(),
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        if self._payout is not None:
            self._payout.unlock()

        self._time_tags.closed(occurred_at)
        self._status = StatusDeal.CANCELLED  

    def _add_payout(self, payout: Payout) -> None:
        self._payout = payout

    def _edit_entries_statuses(self, status: EntryStatus) -> None:
        for entry in self._deal_entries:
            entry.update_status(status)

    def __repr__(self) -> str:
        return (
            f'DisputeDeal('
                f'deal_id={self._deal_id}, '
                f'buyer_id={self._buyer_id}, ' 
                f'seller_id={self._seller_id}, '
                f'price={self._price}, ' 
                f'time_tags={self._time_tags}, '
                f'deadlines={self._deadlines}, ' 
                f'deal_entries={self._deal_entries}, ' 
                f'status={self._status}, '
                f'is_disputed={self._is_disputed}, '
                f'payout={self._payout}'
            ')'
        )
    
    def __eq__(self, other: 'DisputeDeal') -> bool:
        if not isinstance(other, DisputeDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)