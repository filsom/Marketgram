from datetime import datetime, timedelta

from marketgram.common.entity import Entity
from marketgram.trade.domain.model.events import (
    BuyerClosedDisputeEvent,
    SellerShippedItemManuallyEvent, 
    SellerShippedReplacementWithAutoShipmentEvent, 
    SellerClosedDisputeWithRefundEvent
)
from marketgram.trade.domain.model.notifications import (
    AdminJoinNotification, 
    ShippedReplacementByDisputeNotification
)
from marketgram.trade.domain.model.p2p.deal.claim import ReturnType
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.unconfirmed_deal import Claim
from marketgram.trade.domain.model.errors import (
    MISSING_DOWNLOAD_LINK, 
    AddLinkError, 
    OpenedDisputeError
)
from marketgram.trade.domain.model.p2p.members import DisputeMembers
from marketgram.trade.domain.model.statuses import StatusDispute


class OpenedDispute(Entity):
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
    ) -> None:
        super().__init__()
        self._dispute_id = dispute_id
        self._card_id = card_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._open_in = open_in
        self._admin_join_in = admin_join_in
        self._status = status
        self._confirm_in = confirm_in

    def provide_replacement(
        self, 
        occurred_at: datetime,
        download_link: str | None = None
    ) -> None:
        if self._claim.return_is_money():
            raise OpenedDisputeError()

        if self._shipment.is_auto_link():
            self.add_event(
                SellerShippedReplacementWithAutoShipmentEvent(
                    self,
                    self._claim.qty_return,
                    occurred_at
                )
            )
        if self._shipment.is_hand():
            if download_link is None:
                raise AddLinkError(MISSING_DOWNLOAD_LINK)
            
            self.add_event(
                SellerShippedItemManuallyEvent(
                    self._dispute_members.deal_id,
                    download_link,
                    occurred_at
                )
            ) 
        self.add_event(
            ShippedReplacementByDisputeNotification(
                self._dispute_members.buyer_id,
                self._dispute_members.deal_id,
                occurred_at
            )
        )
        self._confirm_in = occurred_at + timedelta(hours=1)
        self._status = StatusDispute.PENDING

    def buyer_refund(self, occurred_at: datetime) -> None: 
        self._claim = self._claim.change_return_type(
            ReturnType.MONEY
        )
        self.add_event(
            SellerClosedDisputeWithRefundEvent(
                self._dispute_members.deal_id,
                self._claim.qty_return,
                occurred_at
            )
        )
        self._status = StatusDispute.CLOSED

    def satisfy_seller(self, occurred_at: datetime) -> None:        
        self.add_event(
            BuyerClosedDisputeEvent(
                self._dispute_members.deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.CLOSED

    def add_admin(self, occurred_at: datetime) -> None:        
        if self._status == StatusDispute.OPEN:
            if self._admin_join_in > occurred_at:
                raise OpenedDisputeError()
        
        self.add_event(
            AdminJoinNotification(
                self._dispute_members.deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.ADMIN_JOINED

    def open_again(self) -> None:
        self.clear_events()
        self._confirm_in = None
        self._status = StatusDispute.OPEN

    @property
    def card_id(self) -> int:
        return self._card_id
    
    @property
    def deal_id(self) -> int:
        return self._dispute_members.deal_id
    
    @property
    def status(self) -> int:
        return self._status

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OpenedDispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)