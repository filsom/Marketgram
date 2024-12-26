from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.trade_item.exceptions import (
    DISCOUNT_ERROR, 
    UNACCEPTABLE_DISCOUNT_RANGE, 
    DomainError
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.description import Description


class Card:
    def __init__(
        self,
        owner_id: UUID,
        price: Money,
        description: Description,
        delivery: Delivery,
        deadlines: Deadlines,
        min_price: Money,
        min_discount: Decimal,
        created_at: datetime,
        card_id: int = None,
        dirty_price: Money | None = None,
        is_archived: bool = False,
        is_purchased: bool = False,
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
        self._dirty_price = dirty_price
        self._is_archived = is_archived
        self._is_purchased = is_purchased
    
    def set_discounted_price(self, new_price: Money) -> None:
        initial_price = self._price

        if self._dirty_price is not None:
            initial_price = self._dirty_price

        if initial_price < self._min_price + self._min_price * self._min_discount:
            raise DomainError(DISCOUNT_ERROR)
        
        max_limit = initial_price - initial_price * self._min_discount
        
        if new_price < self._min_price or new_price > max_limit.round_up():
            raise DomainError(
                UNACCEPTABLE_DISCOUNT_RANGE.format(self._min_price, max_limit)
            )   
        
        if self._dirty_price is None:
            self._dirty_price = self._price
            self._price = new_price
        else:
            self._price = new_price

    def remove_discount(self) -> None:
        if self._dirty_price is not None:
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
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def price(self) -> Money:
        return self._price
    
    def __eq__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)