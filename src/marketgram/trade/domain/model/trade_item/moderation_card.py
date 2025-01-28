from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.category import ActionTime
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.description import Description


class ModerationCard:
    def __init__(
        self,
        owner_id: UUID,
        category_id: int,
        price: Money,
        description: Description,
        features: dict,
        action_time: ActionTime,
        init_status_deal: StatusDeal,
        type_deal: TypeDeal,
        created_at: datetime,
        status: StatusCard,
        card_id: int = None,
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._category_id = category_id
        self._price = price
        self._description = description
        self._features = features
        self._action_time = action_time
        self._init_status_deal = init_status_deal
        self._type_deal = type_deal
        self._created_at = created_at
        self._status = status

    def accept(self) -> None:
        self._status = StatusCard.ON_SALE

    def reject(self) -> None:
        self._status = StatusCard.REJECTED

    @property
    def status(self) -> StatusCard:
        return self._status
    
    @property
    def action_time(self) -> ActionTime:
        return self._action_time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModerationCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)