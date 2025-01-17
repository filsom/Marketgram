from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.rule.agreement.entry import PostingEntry
from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class CancellationDeal:
    def __init__(
        self,
        deal_id: int,
        buyer_id: UUID,
        price: Money,
        time_tags: TimeTags,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        self._deal_id = deal_id
        self._buyer_id = buyer_id
        self._price = price
        self._time_tags = time_tags
        self._status = status
        self._entries = entries

    def cancel(self, current_date: datetime) -> None:
        if self._entries:
            for entry in self._entries:
                entry.update_status(EntryStatus.CANCELLED)

        self._entries.append(
            PostingEntry(
                self._buyer_id,
                self._price,
                current_date,
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        self._time_tags.closed(current_date)
        self._status = StatusDeal.CANCELLED
    
    def __eq__(self, other: 'CancellationDeal') -> bool:
        if not isinstance(other, CancellationDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)