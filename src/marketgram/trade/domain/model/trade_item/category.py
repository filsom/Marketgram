from datetime import datetime
from decimal import Decimal

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.moderation_card import (
    ModerationCard, 
    StatusCard
)
from marketgram.trade.domain.model.trade_item1.description import Description


class Category:
    def __init__(
        self,
        service_id: int, 
        category_type_id: int,
        alias: str,
        action_time: ActionTime,
        type_deal: TypeDeal,
        init_status_deal: StatusDeal,
        minimum_price: Money,
        minimum_procent_discount: Decimal,
        category_id: int = None
    ) -> None:
        self._service_id = service_id
        self._category_type_id = category_type_id
        self._alias = alias
        self._action_time = action_time
        self._type_deal = type_deal
        self._init_status_deal = init_status_deal
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount
        self._category_id = category_id    
    
    def new_card(
        self, 
        user_id: int,
        description: Description,
        price: Money,
        features: dict, 
        action_time: dict[str, int] | None,
        current_date: datetime
    ) -> ModerationCard:
        if price < self._minimum_price: 
            raise DomainError()

        if action_time:  
            action_time = ActionTime(**action_time)
        else:
            action_time = self._action_time
        
        return ModerationCard(
            user_id,
            self._category_id,
            price,
            description,
            features,
            action_time,
            self._init_status_deal,
            self._type_deal,
            current_date,
            StatusCard.ON_MODERATION
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
    def type_deal(self) -> TypeDeal:
        return self._type_deal
    
    @property
    def init_status_deal(self) -> StatusDeal:
        return self._init_status_deal
    
    @property
    def minimum_price(self) -> Money:
        return self._minimum_price
    
    @property
    def minimum_procent_discount(self) -> Decimal:
        return self._minimum_procent_discount 
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return False

        return self.category_id == other.category_id
    
    def __hash__(self) -> int:
        return hash(self.category_id)