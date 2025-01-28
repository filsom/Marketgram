from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard, StatusCard
from marketgram.trade.domain.model.trade_item1.description import Description


class Category:
    def __init__(
        self,
        name: str,
        alias: str,
        action_time: ActionTime,
        is_auto: bool,
        is_time_fixe: bool,
        init_status_deal: StatusDeal,
        minimum_price: Money,
        minimum_procent_discount: Decimal,
        subcategory: list[Category],
        category_id: int = None
    ) -> None:
        self._name = name
        self._alias = alias
        self._action_time = action_time
        self._is_auto = is_auto
        self._is_time_fixe = is_time_fixe
        self._init_status_deal = init_status_deal
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount
        self._subcategory = subcategory
        self._category_id = category_id    
    
    def new_card(
        self, 
        user_id: int,
        description: Description,
        price: Money,
        features: dict, 
        current_date: datetime,
        action_time: dict | None
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
            current_date,
            StatusCard.ON_MODERATION
        )