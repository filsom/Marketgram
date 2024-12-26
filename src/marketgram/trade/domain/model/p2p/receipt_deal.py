from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags


class ReceiptDeal:
    def __init__(
        self, 
        deal_id: UUID,
        time_tags: TimeTags,
        deadlines: Deadlines,
        status: StatusDeal
    ) -> None:
        self._deal_id = deal_id
        self._time_tags = time_tags
        self._deadlines = deadlines
        self._status = status

    def confirm_receipt(self, occurred_at: datetime) -> None:
        if self.receipt_deadline() < occurred_at:
            raise DomainError()
        
        self._time_tags.received(occurred_at)
        self._status = StatusDeal.CHECK

    def receipt_deadline(self) -> datetime:
        return (self._time_tags.shipped_at 
                + self._deadlines.total_receipt_hours)

    def __eq__(self, other: 'ReceiptDeal') -> bool:
        if not isinstance(other, ReceiptDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)