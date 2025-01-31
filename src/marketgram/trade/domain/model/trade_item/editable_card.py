from decimal import Decimal

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.trade_item.category import ActionTime
from marketgram.trade.domain.model.trade_item.description import (
    Description, 
    StatusDescription
)
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.exceptions import (
    DISCOUNT_ERROR, 
    UNACCEPTABLE_DISCOUNT_RANGE
)


class EditableCard:
    def __init__(
        self,
        card_id: int,
        price: Money,
        init_price: Money,
        action_time: ActionTime,
        shipment: Shipment,
        minimum_price: Money,
        minimum_procent_discount: Decimal,
        status: StatusCard,
        descriptions: list[Description]
    ) -> None:
        self._card_id = card_id
        self._price = price
        self._init_price = init_price
        self._action_time = action_time
        self._shipment = shipment
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount
        self._status = status
        self._descriptions = descriptions

    def set_discounted_price(self, new_price: Money) -> None:
        if self._init_price < (self._minimum_price 
                                + self._minimum_price 
                                * self._minimum_procent_discount):
            raise DomainError(DISCOUNT_ERROR)
        
        max_limit = self._init_price - self._init_price * self._minimum_procent_discount
        
        if new_price < self._minimum_price or new_price > max_limit.round_up():
            raise DomainError(
                UNACCEPTABLE_DISCOUNT_RANGE.format(self._minimum_price, max_limit)
            )
        self._price = new_price

    def remove_discount(self) -> None:
        self._price = self._init_price

    def put_on_sale(self) -> None:
        self._status = StatusCard.ON_SALE

    def add_new_description(self, name: str, body: str) -> None:
        new_description = Description(self._card_id, name, body, StatusDescription.NEW)
        if not self._descriptions:
            self._descriptions.append(new_description)
            return 
        
        for description in self._descriptions:
            if description.status == StatusDescription.NEW:
                raise DomainError()
        
        self._descriptions.append(new_description)
        self._status = StatusCard.ON_MODERATION

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EditableCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)