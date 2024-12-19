from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
from uuid import UUID

from marketgram.trade.domain.model.exceptions import (
    DISCOUNT_ERROR, 
    UNACCEPTABLE_DISCOUNT_RANGE, 
    DomainError
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.description import Description


class StorageType(StrEnum):
    STORED = auto()
    NOT_STORED = auto()


class Card:
    def __init__(
        self,
        card_id: UUID,
        owner_id: UUID,
        price: Money,
        description: Description,
        delivery: Delivery,
        deadlines: Deadlines,
        min_price: Money,
        min_discount: Decimal,
        created_at: datetime
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._price = price
        self._description = description
        self._delivery = delivery
        self._deadlines = deadlines
        self._min_price = min_price
        self._min_discount = min_discount
        self._created_at = created_at
        self._dirty_price: Money | None = None
        self._is_archived = False
        self._is_purchased = False
        self._is_storage = StorageType.NOT_STORED
        # self._inventory_balances = []

    def set_discount(self, new_price: Money) -> None:
        initial_price = self._price

        if self._dirty_price is not None:
            initial_price = self._dirty_price

        min_limit, max_limit = self._discount_range(initial_price)
        if new_price < min_limit or new_price > max_limit:
            raise DomainError(
                UNACCEPTABLE_DISCOUNT_RANGE.format(min_limit, max_limit)
            )    
        self._update_price(new_price)

    def add_inventory_balances(self):
        # Доделать
        
        # if not self._delivery.is_auto_link():
        #     raise DomainError()
        
        # self._inventory_balances.append(...)
        # self._is_storage = StorageType.STORED
        pass

    def remove_discount(self) -> None:
        self._price = self._dirty_price
        self._dirty_price = None

    def change_description(self, description: Description) -> None:
        self._description = description

    def archive(self) -> None:
        self._is_archived = True

    def show(self) -> None:
        self._is_archived = False
    
    @property
    def card_id(self) -> UUID:
        return self._card_id
    
    @property
    def owner_id(self) -> UUID:
        return self._owner_id
    
    @property
    def price(self) -> Money:
        return self._price

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def _update_price(self, new_price: Money) -> None:
        if self._dirty_price is None:
            self._dirty_price = self._price
            self._price = new_price
        else:
            self._price = new_price

    def _discount_range(self, price: Money) -> Money:
        if price < self._min_price + self._min_price * self._min_discount:
            raise DomainError(DISCOUNT_ERROR)
        
        max_limit = price - price * self._min_discount

        return self._min_price, max_limit.round_up()

    def __eq__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)