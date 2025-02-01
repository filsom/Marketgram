from datetime import datetime

from marketgram.trade.domain.model.events import PurchasedCardWithHandProvidingNotification, ShippedByDealNotification
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.money import Money


class ShipDeal:
    def __init__(
        self,
        card_id: int,
        members: Members,
        qty_purchased: int,
        shipment: Shipment,
        price: Money,
        deadlines: Deadlines,
        status: StatusDeal,
        created_at: datetime,
        deal_id: int = None,
        download_link: str = None,
        shipped_at: datetime = None
    ) -> None:
        self._deal_id = deal_id
        self._card_id = card_id
        self._members = members
        self._qty_purchased = qty_purchased
        self._shipment = shipment
        self._price = price
        self._deadlines = deadlines
        self._status = status
        self._created_at = created_at
        self._download_link = download_link
        self._shipped_at = shipped_at
        self.events = []

    def confirm_shipment(
        self, 
        occurred_at: datetime
    ) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise DomainError()
        
        if self._shipment.is_link():
            if self._download_link is None:
                raise DomainError()
        
        if not self._shipment.is_message():
            self.events.append(
                ShippedByDealNotification(
                    self._members.buyer_id,
                    self._deal_id,
                    self._download_link,
                    occurred_at
                )
            )
        self._shipped_at = occurred_at
        self._status = StatusDeal.INSPECTION

    def add_download_link(
        self, 
        link: str,  
        occurred_at: datetime
    ) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise DomainError()
        
        if self._shipment.is_auto_link():
            if self._download_link is None:
                self._download_link = link
                return 
            else:
                raise DomainError()
                    
        if self._shipment.is_message():
            raise DomainError()
        
        if self._download_link is not None:
            raise DomainError()
        
        self._download_link = link

    def can_notify_seller(self) -> None:
        if self._shipment.is_hand():
            self.events.append(
                PurchasedCardWithHandProvidingNotification(
                    self._members.seller_id,
                    self._deal_id,
                    self._qty_purchased,
                    self._shipped_at,
                    self._created_at
                )
            )

    @property
    def buyers_debt(self) -> Money:
        return -self._price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ShipDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)