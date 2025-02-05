from datetime import datetime
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.description import (
    Description, 
    StatusDescription
)
from marketgram.trade.domain.model.trade_item.moderation_card import ModerationCard
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class PurchasedCard:
    def __init__(
        self,
        card_id: int,
        owner_id: int,
        category_id: int,
        _unit_price: Money,
        descriptions: list[Description],
        features: dict,
        action_time: ActionTime,
        shipment: Shipment,
        created_at: datetime,
        status: StatusCard
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._category_id = category_id
        self._unit_price = _unit_price
        self._descriptions = descriptions
        self._features = features
        self._action_time = action_time
        self._shipment = shipment
        self._created_at = created_at
        self._status = status

    def reissue(self, current_time: datetime) -> ModerationCard:
        for description in self._descriptions:
            if description.status == StatusDescription.CURRENT:
                return ModerationCard(
                    self._owner_id,
                    self._category_id,
                    self._unit_price,
                    self._unit_price,
                    description,
                    self._features,
                    self._action_time,
                    self._shipment,
                    current_time,
                    StatusCard.ON_SALE
                )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PurchasedCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)