from datetime import datetime

from marketgram.trade.domain.model.events import (
    AdminShippedReplacementWithAutoShipmentEvent, 
    AdminClosedDisputeWithRefundEvent
)
from marketgram.trade.domain.model.p2p.deal.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.status_dispute import StatusDispute
from marketgram.trade.domain.model.p2p.members import DisputeMembers


class AdminDispute:
    def __init__(
        self,
        dispute_id: int,
        card_id: int,
        claim: Claim,
        dispute_members: DisputeMembers,
        shipment: Shipment,
        status: StatusDispute,
        download_link: str | None
    ) -> None:
        self._dispute_id = dispute_id
        self._card_id = card_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._status = status
        self._download_link = download_link
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
                self._status = StatusDispute.PENDING
                return 
            
            elif self._shipment.is_not_auto_link():
                self._claim = self._claim.change_return_type(
                    ReturnType.MONEY
                )
            
        elif self._claim.return_is_money():
            self.buyer_refund(occurred_at)

        self._status = StatusDispute.CLOSED
        
    def buyer_refund(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            self._claim = self._claim.change_return_type(ReturnType.MONEY)

        self.events.append(
            AdminClosedDisputeWithRefundEvent(
                self._dispute_members.deal_id,
                self._claim.qty_return,
                occurred_at
            )
        )
        if self._status != StatusDispute.CLOSED:
            self._status = StatusDispute.CLOSED

    def add_download_link(self, download_link: str) -> None:
        self._download_link = download_link

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AdminDispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)