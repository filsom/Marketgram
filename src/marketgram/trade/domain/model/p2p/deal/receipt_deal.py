from datetime import datetime

from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal


class ReceiptDeal:
    def __init__(
        self, 
        deal_id: int,
        deadlines: Deadlines,
        status: StatusDeal
    ) -> None:
        self._deal_id = deal_id
        self._deadlines = deadlines
        self._status = status

    def confirm_receipt(self, occurred_at: datetime) -> None:
        if self._deadlines.receipt < occurred_at:
            raise DomainError()
        
        self._status = StatusDeal.CHECK

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReceiptDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)