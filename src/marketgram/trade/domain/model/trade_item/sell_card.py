from datetime import datetime

from marketgram.trade.domain.model.notifications import (
    ReissuePurchasedCardNotification
)
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.errors import (
    QuantityItemError, 
    ReplacingItemError, 
    CurrentСardStateError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import StatusCard, StatusDeal
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class SellCard:
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        unit_price: Money,
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._unit_price = unit_price
        self._shipment = shipment
        self._action_time = action_time
        self._status = status
        self.events = []

    def purchase(
        self, 
        buyer_id: int, 
        price: Money,
        shipment: Shipment,
        quantity: int, 
        occurred_at: datetime
    ) -> ShipDeal:
        self._can_purchase(price, shipment)
        
        if quantity <= 0:
            raise QuantityItemError()
        
        self._status = StatusCard.PURCHASED
        self.events.append(
            ReissuePurchasedCardNotification(
                self._owner_id,
                self._card_id,
                occurred_at
            )
        )
        return ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            quantity,
            self._shipment,
            self._unit_price,
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )
            
    def edit(self) -> None:
        self._status = StatusCard.EDITING

    def replace(
        self, 
        qty_replacement: int, 
        occurred_at: datetime
    ) -> None:
        raise ReplacingItemError()

    def _can_purchase(self, price: Money, shipment: Shipment) -> None:
        if self._status != StatusCard.ON_SALE:
            raise CurrentСardStateError()
        
        if price != self._unit_price:
            raise CurrentСardStateError()
    
    @property
    def price(self) -> Money:
        return self._unit_price
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SellCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)