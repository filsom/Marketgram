from datetime import datetime, timedelta

from marketgram.common.entity import Entity
from marketgram.trade.domain.model.events import (
    AdminClosedDisputeWithRefundEvent,
    AdminShippedReplacementWithAutoShipmentEvent,
    BuyerClosedDisputeEvent,
    BuyerConfirmedAndClosedDisputeEvent,
    SellerShippedItemManuallyEvent, 
    SellerShippedReplacementWithAutoShipmentEvent, 
    SellerClosedDisputeWithRefundEvent
)
from marketgram.trade.domain.model.notifications import (
    AdminJoinNotification,
    BuyerRejectedReplacementNotification, 
    ShippedReplacementByDisputeNotification
)
from marketgram.trade.domain.model.p2p.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.errors import (
    MISSING_DOWNLOAD_LINK, 
    AddLinkError,
    CheckDeadlineError, 
    OpenedDisputeError
)
from marketgram.trade.domain.model.p2p.members import DisputeMembers
from marketgram.trade.domain.model.statuses import StatusDispute


class Dispute(Entity):
    def __init__(
        self, 
        dispute_id: int | None,
        card_id: int
    ) -> None:
        super().__init__()
        self._dispute_id = dispute_id
        self._card_id = card_id
    
    @property
    def card_id(self) -> int:
        return self._card_id
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dispute):
            return False

        return self._dispute_id == other._dispute_id
    
    def __hash__(self) -> int:
        return hash(self._dispute_id)


class OpenedDispute(Dispute):
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
        super().__init__(dispute_id, card_id)
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
    def deal_id(self) -> int:
        return self._dispute_members.deal_id
    
    @property
    def status(self) -> int:
        return self._status
    

class PendingDispute(Dispute):
    def __init__(
        self,
        dispute_id: int,
        deal_id: int,
        card_id: int,
        claim: Claim,
        status: StatusDispute,
        confirm_in: datetime,
    ) -> None:
        super().__init__(dispute_id, card_id)
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
    

class AdminDispute(Dispute):
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
        super().__init__(dispute_id, card_id)
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._status = status
        self._confirm_in = confirm_in

    def satisfy_buyer(self, occurred_at: datetime) -> None:
        if self._claim.is_replacement():
            if self._shipment.is_auto_link():
                self.add_event(
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

        self.add_event(
            AdminClosedDisputeWithRefundEvent(
                self._dispute_members.deal_id,
                self._claim.qty_return,
                occurred_at
            )
        )
        if self._status != StatusDispute.CLOSED:
            self._status = StatusDispute.CLOSED
    
    @property
    def deal_id(self) -> int:
        return self._dispute_members.deal_id