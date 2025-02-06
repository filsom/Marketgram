from datetime import datetime, timedelta

from marketgram.trade.domain.model.events import (
    AdminShippedReplacementWithAutoShipmentEvent, 
    AdminClosedDisputeWithRefundEvent
)
from marketgram.trade.domain.model.p2p.deal.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.members import DisputeMembers
from marketgram.trade.domain.model.statuses import StatusDispute


class AdminDispute:
    def __init__(
        self,
        dispute_id: int,
        card_id: int,
        claim: Claim,
        dispute_members: DisputeMembers,
        shipment: Shipment,
        status: StatusDispute,
        confirm_in: datetime | None
    ) -> None:
        self._dispute_id = dispute_id
        self._card_id = card_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._status = status
        self._confirm_in = confirm_in
        self.events = []   

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            if self._shipment.is_auto_link():
                self.events.append(
                    AdminShippedReplacementWithAutoShipmentEvent(
                        self,
                        self._claim.qty_return,
                        occurred_at
                    )
                )
                self._confirm_in = occurred_at + timedelta(hours=1)
                self._status = StatusDispute.PENDING
                return 
            
        self.buyer_refund(occurred_at)
        self._status = StatusDispute.CLOSED
        
    def buyer_refund(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            self._claim = self._claim.change_return_type(
                ReturnType.MONEY
            )
            self._confirm_in = None

        self.events.append(
            AdminClosedDisputeWithRefundEvent(
                self._dispute_members.deal_id,
                self._claim.qty_return,
                occurred_at
            )
        )
        if self._status != StatusDispute.CLOSED:
            self._status = StatusDispute.CLOSED

    @property
    def card_id(self) -> int:
        return self._card_id
    
    @property
    def deal_id(self) -> int:
        return self._dispute_members.deal_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AdminDispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)