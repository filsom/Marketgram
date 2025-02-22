from datetime import datetime
from decimal import Decimal

from marketgram.common.entity import Entity
from marketgram.common.errors import DomainError
from marketgram.trade.domain.model.entries import InventoryEntry
from marketgram.trade.domain.model.errors import (
    DISCOUNT_ERROR, 
    UNACCEPTABLE_DISCOUNT_RANGE
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.notifications import (
    AdminRejectedModerationCardNotification, 
    InventoryBalancesAddedNotification
)
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.types import InventoryOperation


class Card(Entity):
    def __init__(self, card_id: int | None) -> None:
        super().__init__()
        self._card_id = card_id

    @property
    def card_id(self) -> int | None:
        return self._card_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)
    

class EditCard(Card):
    def __init__(
        self,
        card_id: int,
        unit_price: Money,
        init_price: Money,
        action_time: ActionTime,
        shipment: Shipment,
        minimum_price: Money,
        minimum_procent_discount: Decimal,
        status: StatusCard,
    ) -> None:
        super().__init__(card_id)
        self._unit_price = unit_price
        self._init_price = init_price
        self._action_time = action_time
        self._shipment = shipment
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount
        self._status = status

    def set_discounted_price(self, new_unit_price: Money) -> None:
        if self._init_price < (self._minimum_price 
                                + self._minimum_price 
                                * self._minimum_procent_discount):
            raise DomainError(DISCOUNT_ERROR)
        
        max_limit = self._init_price - self._init_price * self._minimum_procent_discount
        
        if new_unit_price < self._minimum_price or new_unit_price > max_limit.round_up():
            raise DomainError(
                UNACCEPTABLE_DISCOUNT_RANGE.format(self._minimum_price, max_limit)
            )
        self._unit_price = new_unit_price

    def remove_discount(self) -> None:
        self._unit_price = self._init_price

    def put_on_sale(self) -> None:
        self._status = StatusCard.ON_SALE

    def can_add_item(self) -> bool:
        return self._shipment != Shipment.CHAT
    

class ModerationCard(Card):
    def __init__(
        self,
        owner_id: int,
        category_id: int,
        unit_price: Money,
        init_price: Money,
        name: str,
        body: str,
        features: dict,
        action_time: ActionTime,
        shipment: Shipment,
        created_at: datetime,
        status: StatusCard,
        inventory_entries: list[InventoryEntry] | None = None,
        card_id: int | None = None,
    ) -> None:
        super().__init__(card_id)
        self._owner_id = owner_id
        self._category_id = category_id
        self._unit_price = unit_price
        self._init_price = init_price
        self._name = name
        self._body = body
        self._features = features
        self._action_time = action_time
        self._shipment = shipment
        self._created_at = created_at
        self._status = status
        self._inventory_entries = inventory_entries

    def accept(self) -> None:
        self._status = StatusCard.ON_SALE

    def reject(self, reason: str, occurred_at: datetime) -> None:        
        self._status = StatusCard.REJECTED
        self.add_event(
            AdminRejectedModerationCardNotification(
                self._card_id,
                self._status,
                reason,
                occurred_at
            )
        )

    def add_stock_item(
        self,
        qty_item: int,
        occurred_at: datetime
    ) -> None:
        if self._shipment.is_hand():
            self._shipment = Shipment.AUTO

        self.add_event(
            InventoryBalancesAddedNotification(
                self._card_id,
                self._owner_id,
                qty_item,
                self._status,
                occurred_at
            )
        )
        self._inventory_entries.append(
            InventoryEntry(
                qty_item,
                occurred_at,
                InventoryOperation.UPLOADING
            )
        )

    @property
    def status(self) -> StatusCard:
        return self._status
    
    @property
    def action_time(self) -> ActionTime:
        return self._action_time
    

class PurchasedCard(Card):
    def __init__(
        self,
        card_id: int,
        status: StatusCard
    ) -> None:
        super().__init__(card_id)
        self._status = status

    def reissue(self) -> None:
        self._status = StatusCard.ON_SALE