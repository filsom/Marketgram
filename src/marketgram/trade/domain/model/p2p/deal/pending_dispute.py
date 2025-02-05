from datetime import datetime

from marketgram.trade.domain.model.events import (
    BuyerConfirmedAndClosedDispute, 
    BuyerRejectedReplacement
)
from marketgram.trade.domain.model.p2p.deal.claim import Claim
from marketgram.trade.domain.model.p2p.deal.status_dispute import StatusDispute
from marketgram.trade.domain.model.p2p.errors import CheckDeadlineError


class PendingDispute:
    def __init__(
        self,
        dispute_id: int,
        deal_id: int,
        claim: Claim,
        status: StatusDispute,
        confirm_in: datetime,
    ) -> None:
        self._dispute_id = dispute_id
        self._deal_id = deal_id
        self._claim = claim
        self._status = status
        self._confirm_in = confirm_in
        self.events = []

    def confirm(self, occurred_at: datetime) -> None:
        if self._confirm_in < occurred_at:
            raise CheckDeadlineError()
        
        self.events.append(
            BuyerConfirmedAndClosedDispute(
                self._deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.CLOSED

    def reject_replacement(self, occurred_at: datetime) -> None:
        if self._confirm_in < occurred_at:
            raise CheckDeadlineError()
        
        self.events(
            BuyerRejectedReplacement(
                self._deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.ADMIN_JOINED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PendingDispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)