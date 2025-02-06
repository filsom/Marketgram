from datetime import datetime
from decimal import Decimal

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.description import Description
from marketgram.trade.domain.model.trade_item.moderation_card import (
    ModerationCard, 
)


class Category:
    def __init__(
        self,
        service_id: int, 
        category_type_id: int,
        alias: str,
        action_time: ActionTime,
        shipment: Shipment,
        minimum_unit_price: Money,
        minimum_procent_discount: Decimal,
        category_id: int | None = None
    ) -> None:
        self._category_id = category_id    
        self._service_id = service_id
        self._category_type_id = category_type_id
        self._alias = alias
        self._action_time = action_time
        self._shipment = shipment
        self._minimum_unit_price = minimum_unit_price
        self._minimum_procent_discount = minimum_procent_discount
    
    def new_card(
        self, 
        user_id: int,
        description: Description,
        unit_price: Money,
        features: dict, 
        action_time: ActionTime | None,
        current_date: datetime
    ) -> ModerationCard:
        if unit_price < self._minimum_unit_price: 
            raise DomainError()
        
        if action_time is None:  
            action_time = self._action_time
        
        return ModerationCard(
            user_id,
            self._category_id,
            unit_price,
            unit_price,
            [description],
            features,
            action_time,
            self._shipment,
            current_date,
            StatusCard.ON_FIRST_MODERATION
        )
    
    @property
    def category_id(self) -> int:
        return self._category_id
    
    @property
    def service_id(self) -> int:
        return self._service_id
    
    @property
    def category_type_id(self) -> int:
        return self._category_type_id
    
    @property
    def action_time(self) -> ActionTime:
        return self._action_time
    
    @property
    def minimum_price(self) -> Money:
        return self._minimum_unit_price
    
    @property
    def minimum_procent_discount(self) -> Decimal:
        return self._minimum_procent_discount 
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return False

        return self.category_id == other.category_id
    
    def __hash__(self) -> int:
        return hash(self.category_id)