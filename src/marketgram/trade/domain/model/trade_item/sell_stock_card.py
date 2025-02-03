from datetime import datetime
from uuid import UUID

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.events import (
    PurchasedCardWithAutoShipmentEvent, 
    ZeroInventoryBalanceNotification
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.inventory_entry import (
    InventoryEntry, 
    InventoryOperation
)
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class SellStockCard(SellCard):
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        price: Money,
        shipment: Shipment,
        action_time: ActionTime,
        status: StatusCard,
        stock_balance: int,
        inventory_entries: list[InventoryEntry]
    ) -> None:
        super().__init__(
            card_id, 
            owner_id, 
            price, 
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
        if quantity <= 0:
            raise DomainError()
        
        remainder = self._stock_balance - quantity
        if remainder < 0:
            raise DomainError()
        
        if remainder == 0:
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
                InventoryOperation.BUY
            )
        )
        deal = ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            quantity,
            self._shipment,
            self._price * quantity,
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )  
        self._status = StatusCard.PURCHASED
        self.events.append(
            PurchasedCardWithAutoShipmentEvent(deal, occurred_at)
        )
        return deal