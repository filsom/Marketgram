from datetime import datetime

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.trade_item.exceptions import (
    DomainError,
    InvalidOperationError,
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.spa.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money


class ShipDeal:
    def __init__(
        self,
        members: Members,
        card_id: int,
        qty_purchased: int,
        type_deal: TypeDeal,
        card_created_at: datetime,
        price: Money,
        time_tags: TimeTags,
        deadlines: Deadlines,
        status: StatusDeal,
        deal_id: int = None,
        is_disputed: bool = False
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._card_id = card_id
        self._qty_purchased = qty_purchased
        self._type_deal = type_deal
        self._price = price
        self._card_created_at = card_created_at
        self._time_tags = time_tags
        self._deadlines = deadlines
        self._status = status
        self._is_disputed = is_disputed

    def confirm_shipment(self, occurred_at: datetime) -> None:
        raise InvalidOperationError()
    
    def delivery_deadline(self) -> datetime:
        return (self._time_tags.created_at
                + self._deadlines.total_shipping_hours)

    def __eq__(self, other: 'ShipDeal') -> bool:
        if not isinstance(other, ShipDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)


class ShipLoginCodeDeal(ShipDeal):
    def confirm_shipment(self, occurred_at: datetime) -> None:
        if self.delivery_deadline() < occurred_at:
            raise DomainError()
                
        self._time_tags = self._time_tags \
            .shipped(occurred_at) \
            .received(occurred_at)
            
        self._status = StatusDeal.CHECK


class ShipProvidingLinkDeal(ShipDeal):
    def confirm_shipment(self, occurred_at: datetime) -> None:
        if self.delivery_deadline() < occurred_at:
            raise DomainError()
                
        self._time_tags = self._time_tags \
            .shipped(occurred_at)
            
        self._status = StatusDeal.AWAITING