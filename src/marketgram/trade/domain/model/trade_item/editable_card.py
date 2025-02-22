from decimal import Decimal

from marketgram.common.errors import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.category import ActionTime
from marketgram.trade.domain.model.trade_item.description import (
    Description, 
    StatusDescription
)
from marketgram.trade.domain.model.errors import (
    DISCOUNT_ERROR, 
    UNACCEPTABLE_DISCOUNT_RANGE
)


class EditableCard:
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
        descriptions: list[Description]
    ) -> None:
        self._card_id = card_id
        self._unit_price = unit_price
        self._init_price = init_price
        self._action_time = action_time
        self._shipment = shipment
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount
        self._status = status
        self._descriptions = descriptions

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

    def add_new_description(self, name: str, body: str) -> None: 
        for description in self._descriptions:
            if description.status == StatusDescription.NEW:
                raise DomainError()
            
        for field in [name, body]:
            if len(field) < 10:
                raise DomainError()
        
        self._descriptions.append(
            Description(
                self._card_id, 
                name, 
                body, 
                StatusDescription.NEW
            )    
        )
        self._status = StatusCard.ON_MODERATION

    def can_add_item(self) -> bool:
        return self._shipment != Shipment.CHAT

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EditableCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)