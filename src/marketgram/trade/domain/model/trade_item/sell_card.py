from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.trade_item.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money


class SellCard:
    def __init__(
        self,
        card_id: int,
        owner_id: UUID,
        price: Money,
        is_archived: bool,
        is_purchased: bool,
        created_at: datetime,
        delivery: Delivery,
        deadlines: Deadlines
    ) -> None:
        self._card_id = card_id
        self._owner_id = owner_id
        self._price = price
        self._is_archived = is_archived
        self._is_purchased = is_purchased
        self._created_at = created_at
        self._deadlines = deadlines
        self._delivery = delivery

    def buy(self, quantity: int) -> None:
        if quantity <= 0:
            raise DomainError()
        
        if self._is_archived:
            raise DomainError()
        
        if self._is_purchased:
            raise DomainError()
        
        self._is_purchased = True

    def time_tags(self, current_time: datetime) -> TimeTags:
        return self._delivery.provide_time_tags(current_time)

    @property
    def deadlines(self) -> Deadlines:
        return self._deadlines
    
    @property
    def status_deal(self) -> StatusDeal:
        return self._delivery.what_stage()

    @property
    def type_deal(self) -> TypeDeal:
        return self._delivery.what_type()

    @property
    def card_id(self) -> UUID:
        return self._card_id
    
    @property
    def owner_id(self) -> UUID:
        return self._owner_id
    
    @property
    def price(self) -> Money:
        return self._price
    
    @property
    def created_in(self) -> datetime:
        return self._created_at

    def __eq__(self, other: 'SellCard') -> bool:
        if not isinstance(other, SellCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)