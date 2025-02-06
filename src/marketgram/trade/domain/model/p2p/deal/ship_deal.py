from datetime import datetime

from marketgram.trade.domain.model.notifications import (
    DealCreatedNotification,
    ShippedByDealNotification,
)
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.errors import (
    MISSING_DOWNLOAD_LINK,
    OVERDUE_SHIPMENT,
    AddLinkError, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import StatusDeal


class ShipDeal:
    def __init__(
        self,
        card_id: int,
        members: Members,
        qty_purchased: int,
        shipment: Shipment,
        unit_price: Money,
        deadlines: Deadlines,
        status: StatusDeal,
        created_at: datetime,
        deal_id: int = None,
        shipped_at: datetime = None
    ) -> None:
        self._deal_id = deal_id
        self._card_id = card_id
        self._members = members
        self._qty_purchased = qty_purchased
        self._shipment = shipment
        self._unit_price = unit_price
        self._deadlines = deadlines
        self._status = status
        self._created_at = created_at
        self._shipped_at = shipped_at
        self.events = []

    def confirm_shipment(
        self, 
        occurred_at: datetime,
        download_link: str | None = None
    ) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise CheckDeadlineError(OVERDUE_SHIPMENT)
            
        if self._shipment.is_not_auto_link():
            if self._shipment.is_hand():
                if download_link is None:
                    raise AddLinkError(MISSING_DOWNLOAD_LINK)    
                
            self.events.append(
                ShippedByDealNotification(
                    self._members.buyer_id,
                    self._deal_id,
                    occurred_at
                )
            )
        self._shipped_at = occurred_at
        self._status = StatusDeal.INSPECTION

    def notify_seller(self) -> None:
        if self._shipment.is_notify_to_the_seller():
            self.events.append(
                DealCreatedNotification(
                    self._members.seller_id,
                    self._deal_id,
                    self._card_id,
                    self._qty_purchased,
                    self._shipped_at,
                    self._created_at
                )
            )

    @property
    def write_off_ammount(self) -> Money:
        return -self._unit_price * self._qty_purchased
    
    @property
    def status(self) -> StatusDeal:
        return self._status
    
    @property
    def shipped_at(self) -> datetime | None:
        return self._shipped_at
    
    @property
    def deal_id(self) -> int:
        return self._deal_id
    
    @property 
    def qty_purchased(self) -> int:
        return self._qty_purchased

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ShipDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)