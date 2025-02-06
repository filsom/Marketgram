from datetime import datetime

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.events import (
    PurchasedCardWithAutoShipmentEvent, 
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.notifications import ZeroInventoryBalanceNotification
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.errors import QuantityItemError
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.statuses import StatusCard, StatusDeal
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.entries import (
    InventoryEntry, 
    InventoryOperation
)
from marketgram.trade.domain.model.trade_item.sell_card import SellCard


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
        quantity: int, 
        occurred_at: datetime
    ) -> ShipDeal:
        self._take_inventory(
            quantity, 
            InventoryOperation.BUY, 
            occurred_at
        )
        deal = ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            quantity,
            self._shipment,
            self._unit_price,
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )  
        self.events.append(
            PurchasedCardWithAutoShipmentEvent(deal, occurred_at)
        )
        return deal
    
    def replace(
        self, 
        qty_replacement: int, 
        occurred_at: datetime
    ) -> None:
        self._take_inventory(
            qty_replacement, 
            InventoryOperation.REPLACE, 
            occurred_at
        )
        
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
            raise DomainError()
        
        if remainder == 0:
            self._shipment = Shipment.HAND
            self._status = StatusCard.EDITING
            self.events.append(
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