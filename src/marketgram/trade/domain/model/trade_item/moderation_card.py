from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.category import ActionTime
from marketgram.trade.domain.model.trade_item.description import Description, StatusDescription
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class ModerationCard:
    def __init__(
        self,
        owner_id: int,
        category_id: int,
        price: Money,
        init_price: Money,
        descriptions: list[Description],
        features: dict,
        action_time: ActionTime,
        shipment: Shipment,
        created_at: datetime,
        status: StatusCard,
        card_id: int | None = None,
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._category_id = category_id
        self._price = price
        self._init_price = init_price
        self._descriptions = descriptions
        self._features = features
        self._action_time = action_time
        self._shipment = shipment
        self._created_at = created_at
        self._status = status

    def accept(self, current_time: datetime) -> None:
        match self._status:
            case StatusCard.ON_FIRST_MODERATION:
                self._descriptions[0].set(current_time)

            case StatusCard.ON_MODERATION:
                for description in self._descriptions:
                    if description.status == StatusDescription.NEW:
                        description.set(current_time)
                    
                    if description.status == StatusDescription.CURRENT:
                        description.archive(current_time)

        self._status = StatusCard.ON_SALE

    def reject(self) -> None:
        match self._status:
            case StatusCard.ON_FIRST_MODERATION:
                self._status = StatusCard.REJECTED
            
            case StatusCard.ON_MODERATION:
                for description in self._descriptions:
                    if description.status == StatusDescription.NEW:
                        description.cancel()
                
                self._status = StatusCard.ON_SALE

    def add_desciption(self, description: Description) -> None:
        self._descriptions.append(description)

    @property
    def status(self) -> StatusCard:
        return self._status
    
    @property
    def action_time(self) -> ActionTime:
        return self._action_time
    
    @property
    def card_id(self) -> int:
        return self._card_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModerationCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)