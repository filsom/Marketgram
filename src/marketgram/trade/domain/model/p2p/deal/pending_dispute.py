from datetime import datetime

from marketgram.common.domain.model.entity import Entity
from marketgram.trade.domain.model.events import BuyerConfirmedAndClosedDisputeEvent
from marketgram.trade.domain.model.notifications import BuyerRejectedReplacementNotification
from marketgram.trade.domain.model.p2p.deal.claim import Claim, ReturnType
from marketgram.trade.domain.model.errors import CheckDeadlineError
from marketgram.trade.domain.model.statuses import StatusDispute


class PendingDispute(Entity):
    def __init__(
        self,
        dispute_id: int,
        deal_id: int,
        claim: Claim,
        status: StatusDispute,
        confirm_in: datetime,
    ) -> None:
        super().__init__()
        self._dispute_id = dispute_id
        self._deal_id = deal_id
        self._claim = claim
        self._status = status
        self._confirm_in = confirm_in

    def confirm(self, occurred_at: datetime) -> None:
        if self._confirm_in < occurred_at:
            raise CheckDeadlineError()
        
        self.add_event(
            BuyerConfirmedAndClosedDisputeEvent(
                self._deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.CLOSED

    def reject_replacement(self, occurred_at: datetime) -> None:
        if self._confirm_in < occurred_at:
            raise CheckDeadlineError()
        
        self.add_event(
            BuyerRejectedReplacementNotification(
                self._deal_id,
                self._dispute_id,
                occurred_at
            )
        )
        self._claim = self._claim.change_return_type(
            ReturnType.MONEY
        )
        self._status = StatusDispute.ADMIN_JOINED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PendingDispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)