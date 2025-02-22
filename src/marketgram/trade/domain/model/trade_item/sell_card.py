from datetime import datetime
from typing import Any

from marketgram.common.entity import Entity
from marketgram.trade.domain.model.entries import InventoryEntry
from marketgram.trade.domain.model.events import PurchasedCardWithAutoShipmentEvent
from marketgram.trade.domain.model.notifications import (
    ReissuePurchasedCardNotification,
    ZeroInventoryBalanceNotification
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
from marketgram.trade.domain.model.types import InventoryOperation


class SellCard(Entity):
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        unit_price: Money,
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
    ) -> None:
        super().__init__()
        self._card_id = card_id
        self._owner_id = owner_id
        self._unit_price = unit_price
        self._shipment = shipment
        self._action_time = action_time
        self._status = status

    def purchase(
        self, 
        buyer_id: int, 
        price: Money,
        shipment: Shipment,
        qty: int, 
        occurred_at: datetime
    ) -> ShipDeal:
        self._check_condition(price, shipment)
        
        if qty <= 0:
            raise QuantityItemError()
        
        self._status = StatusCard.PURCHASED
        self.add_event(
            ReissuePurchasedCardNotification(
                self._owner_id,
                self._card_id,
                occurred_at
            )
        )
        return ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            qty,
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

    def _check_condition(self, price: Money, shipment: Shipment) -> None:
        if self._status != StatusCard.ON_SALE:
            raise CurrentСardStateError(self.current_conditions)
        
        if price != self._unit_price:
            raise CurrentСardStateError(self.current_conditions)
        
    @property
    def current_conditions(self) -> dict[str, Any]:
        return {
            'card_id': self._card_id,
            'card_status': self._status,
            'price': self._unit_price,
            'type_shipment': self._shipment
        }
    
    @property
    def price(self) -> Money:
        return self._unit_price
    
    @property
    def status(self) -> StatusCard:
        return self._status
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SellCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)
    

class SellStockCard(SellCard):
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        unit_price: Money,
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
        stock_balance: int,
        inventory_entries: list[InventoryEntry]
    ) -> None:
        super().__init__(
            card_id, 
            owner_id, 
            unit_price, 
            shipment, 
            action_time, 
            status
        )
        self._stock_balance = stock_balance
        self._inventory_entries = inventory_entries

    def purchase(
        self, 
        buyer_id: int, 
        price: Money,
        shipment: Shipment,
        qty: int, 
        occurred_at: datetime
    ) -> ShipDeal:
        self._check_condition(price, shipment)
        self._take_inventory(
            qty, 
            InventoryOperation.BUY, 
            occurred_at
        )
        deal = ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            qty,
            self._shipment,
            self._unit_price,
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )  
        self.add_event(
            PurchasedCardWithAutoShipmentEvent(deal, occurred_at)
        )
        return deal

    def replace(self, qty: int, occurred_at: datetime) -> None:
        try:
            self._take_inventory(
                qty, 
                InventoryOperation.REPLACE, 
                occurred_at
            )
        except QuantityItemError:
            raise ReplacingItemError()
        
    def _check_condition(self, price: Money, shipment: Shipment) -> None:
        super()._check_condition(price, shipment)
    
        if self._shipment != shipment:
            raise CurrentСardStateError(self.current_conditions)
        
    def _take_inventory(
        self, 
        quantity: int, 
        operation: InventoryOperation, 
        occurred_at: datetime
    ) -> None:
        if quantity <= 0:
            raise QuantityItemError()
        
        remainder = self._stock_balance - quantity
        if remainder < 0:
            raise QuantityItemError()
        
        if remainder == 0:
            self._shipment = Shipment.HAND
            self._status = StatusCard.PURCHASED
            self.add_event(
                ZeroInventoryBalanceNotification(
                    self._owner_id,
                    self._card_id,
                    occurred_at
                )
            )
        self._inventory_entries.append(
            InventoryEntry(
                -quantity, 
                occurred_at, 
                operation
            )
        )

    @property
    def inventory_entries(self) -> list[InventoryEntry]:
        return self._inventory_entries
    
    @property
    def shipment(self) -> Shipment:
        return self._shipment