from uuid import UUID

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class SellCard:
    def __init__(
        self,
        card_id: int,
        owner_id: UUID,
        price: Money,
        init_status_deal: StatusDeal,
        type_deal: TypeDeal,
        action_time: ActionTime,
        status: StatusCard
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._price = price
        self._init_status_deal = init_status_deal
        self._type_deal = type_deal
        self._action_time = action_time
        self._status = status

    def buy(self, quantity: int) -> None:
        if quantity <= 0:
            raise DomainError()
        
        self._status = StatusCard.PURCHASED
    
    @property
    def status_deal(self) -> StatusDeal:
        return self._init_status_deal

    @property
    def type_deal(self) -> TypeDeal:
        return self._type_deal

    @property
    def card_id(self) -> UUID:
        return self._card_id
    
    @property
    def owner_id(self) -> UUID:
        return self._owner_id
    
    @property
    def price(self) -> Money:
        return self._price

    def __eq__(self, other: 'SellCard') -> bool:
        if not isinstance(other, SellCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)
    

class SellStockCard(SellCard):
    def buy(self, quantity: int) -> None:
        pass