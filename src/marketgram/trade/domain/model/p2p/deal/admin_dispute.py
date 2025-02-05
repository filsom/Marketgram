from datetime import datetime

from marketgram.trade.domain.model.events import AdminClosedDisputeWithAutoShipmentEvent, AdminClosedDisputeWithRefund
from marketgram.trade.domain.model.p2p.deal.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.status_dispute import StatusDispute
from marketgram.trade.domain.model.p2p.members import DisputeMembers


class AdminDispute:
    def __init__(
        self,
        card_id: int,
        claim: Claim,
        dispute_members: DisputeMembers,
        shipment: Shipment,
        open_in: datetime,
        admin_join_in: datetime,
        status: StatusDispute,
        dispute_id: int | None = None,
        confirm_in: datetime | None = None,
        download_link: str | None = None
    ) -> None:
        self._dispute_id = dispute_id
        self._card_id = card_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._open_in = open_in
        self._admin_join_in = admin_join_in
        self._status = status
        self._download_link = download_link
        self._confirm_in = confirm_in
        self.events = []   

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            if self._shipment.is_auto_link():
                self.events.append(
                    AdminClosedDisputeWithAutoShipmentEvent(
                        self,
                        self._claim.qty_return,
                        occurred_at
                    )
                )
        elif self._claim.return_is_money():
            self.buyer_refund(occurred_at)

        self._status = StatusDispute.CLOSED
        
    def buyer_refund(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            self._claim = self._claim.change_return_type(ReturnType.MONEY)

        self.events.append(
            AdminClosedDisputeWithRefund(
                self._dispute_members.deal_id,
                self._claim.qty_return,
                occurred_at
            )
        )
        if self._status != StatusDispute.CLOSED:
            self._status = StatusDispute.CLOSED