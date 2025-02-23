from datetime import datetime
from typing import Any

from marketgram.trade.domain.model.entries import InventoryEntry, PriceEntry
from marketgram.trade.domain.model.events import PurchasedCardWithAutoShipmentEvent
from marketgram.trade.domain.model.notifications import (
    ReissuePurchasedCardNotification,
    ZeroInventoryBalanceNotification
)
from marketgram.trade.domain.model.p2p.deal import ShipDeal
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.errors import (
    QuantityItemError, 
    ReplacingItemError, 
    CurrentСardStateError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import StatusCard, StatusDeal
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.card import Card
from marketgram.trade.domain.model.types import InventoryOperation


class SellCard(Card):
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        price_entries: list[PriceEntry],
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
    ) -> None:
        super().__init__(card_id)
        self._owner_id = owner_id
        self._price_entries = price_entries
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
        if qty <= 0:
            raise QuantityItemError()
        
        self._check_conditions(qty, price, shipment)
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
            self._get_price(qty),
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
    
    def _get_price(self, qty: int) -> Money:
        for price_entry in sorted(self._price_entries):
            if qty >= price_entry.start_qty:
                return price_entry.unit_price

    def _check_conditions(self, qty: int, current_price: Money, shipment: Shipment) -> None:
        conditions = self._current_conditions(qty)
        if self._status != StatusCard.ON_SALE:
            raise CurrentСardStateError(conditions)
        
        if current_price != conditions['current_price']:
            raise CurrentСardStateError(conditions)
        
    def _current_conditions(self, qty: str) -> dict[str, Any]:
        return {
            'card_id': self._card_id,
            'card_status': self._status,
            'current_price': self._get_price(qty),
            'type_shipment': self._shipment
        }
    
    @property
    def status(self) -> StatusCard:
        return self._status
    

class SellStockCard(SellCard):
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        price_entries: list[PriceEntry],
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
        stock_balance: int,
        inventory_entries: list[InventoryEntry]
    ) -> None:
        super().__init__(
            card_id, 
            owner_id, 
            price_entries, 
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
        if qty <= 0:
            raise QuantityItemError()
        
        self._check_conditions(qty, price, shipment)
        self._take_inventory(qty, InventoryOperation.BUY, occurred_at)

        deal = ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            qty,
            self._shipment,
            self._get_price(qty),
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )  
        self.add_event(
            PurchasedCardWithAutoShipmentEvent(deal, occurred_at)
        )
        return deal

    def replace(self, qty: int, occurred_at: datetime) -> None:
        if qty <= 0:
            raise ReplacingItemError()
        
        try:
            self._take_inventory(
                qty, 
                InventoryOperation.REPLACE, 
                occurred_at
            )
        except QuantityItemError:
            raise ReplacingItemError()
        
    def _check_conditions(self, qty: int, price: Money, shipment: Shipment) -> None:
        super()._check_conditions(qty, price, shipment)
        if self._shipment != shipment:
            raise CurrentСardStateError()
        
    def _take_inventory(
        self, 
        quantity: int, 
        operation: InventoryOperation, 
        occurred_at: datetime
    ) -> None:
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