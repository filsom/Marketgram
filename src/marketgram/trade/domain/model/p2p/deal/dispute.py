from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from marketgram.trade.domain.model.events import AdminJoinNotification, BuyerClosedDisputeEvent, SellerClosedDisputeWithAutoShipmentEvent
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.unconfirmed_deal import Claim
from marketgram.trade.domain.model.p2p.errors import AddLinkError, OpenedDisputeError, QuantityItemError
from marketgram.trade.domain.model.p2p.members import DisputeMembers


class StatusDispute(StrEnum):
    OPEN = auto()
    ADMIN_JOINED = auto()
    CLOSED = auto()

    def is_admin_joined(self) -> bool:
        return self == StatusDispute.ADMIN_JOINED


class Dispute:
    def __init__(
        self,
        dispute_id: UUID,
        card_id: int,
        claim: Claim,
        dispute_members: DisputeMembers,
        shipment: Shipment,
        open_in: datetime,
        status: StatusDispute,
        download_link: str | None = None
    ) -> None:
        self._dispute_id = dispute_id
        self._card_id = card_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._shipment = shipment
        self._open_in = open_in
        self._status = status
        self._download_link = download_link
        self.events = []

    def satisfy_buyer(
        self, 
        qty_return: int, 
        download_link: str | None, 
        occurred_at: datetime
    ) -> None:
        if self._status.is_admin_joined():
            raise OpenedDisputeError()
        
        if self._claim.qty_return != qty_return:
            raise QuantityItemError()
        
        if self._claim.is_replacement():
            if self._shipment.is_hand():
                if download_link is None:
                    raise AddLinkError()
            
                self._download_link = download_link

            elif self._shipment.is_auto_link():
                self.events.append(
                    SellerClosedDisputeWithAutoShipmentEvent(
                        self._card_id, 
                        occurred_at
                    )
                )
            elif self._shipment.is_message():
                if download_link is not None:
                    raise AddLinkError()

        elif self._claim.return_is_money():
            pass
            
    def satisfy_seller(self, occurred_at: datetime) -> None:
        if self._status.is_admin_joined():
            raise OpenedDisputeError()
        
        self.events.append(
            BuyerClosedDisputeEvent(
                self._dispute_members.deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.CLOSED

    def add_admin(self, occurred_at: datetime) -> None:
        if self._status.is_admin_joined():
            raise OpenedDisputeError()
        
        self.events.append(
            AdminJoinNotification(
                self._dispute_members.deal_id,
                occurred_at
            )
        )
        self._status = StatusDispute.ADMIN_JOINED