from datetime import datetime

from marketgram.trade.domain.model.entries import InventoryEntry
from marketgram.trade.domain.model.notifications import ReissuePurchasedCardNotification
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.errors import QuantityItemError, ReplacingItemError
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
        inventory_entries: list[InventoryEntry]
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._unit_price = unit_price
        self._shipment = shipment
        self._action_time = action_time
        self._status = status
        self._inventory_entries = inventory_entries
        self.events = []

    def purchase(
        self, 
        buyer_id: int, 
        quantity: int, 
        occurred_at: datetime
    ) -> ShipDeal:
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
    
    @property
    def price(self) -> Money:
        return self._unit_price
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SellCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)