from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.category import ActionTime
from marketgram.trade.domain.model.trade_item.description import Description
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class ModerationCard:
    def __init__(
        self,
        owner_id: UUID,
        category_id: int,
        price: Money,
        descriptions: list[Description],
        features: dict,
        action_time: ActionTime,
        shipment: Shipment,
        created_at: datetime,
        status: StatusCard,
        card_id: int = None,
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._category_id = category_id
        self._price = price
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
                filtred_list = list(filter(
                    lambda description: description.set_in is not None, 
                    self._descriptions
                ))
                sorted_description = sorted(filtred_list)
                sorted_description[-1].set(current_time)
                sorted_description[-2].archive(current_time)

        self._status = StatusCard.ON_SALE

    def reject(self) -> None:
        match self._status:
            case StatusCard.ON_FIRST_MODERATION:
                self._status = StatusCard.REJECTED
            
            case StatusCard.ON_MODERATION:
                self._status = StatusCard.ON_SALE

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