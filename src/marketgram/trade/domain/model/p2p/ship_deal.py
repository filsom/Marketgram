from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from marketgram.trade.domain.model.exceptions import (
    DomainError,
    InvalidOperationError,
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.money import Money

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.user import QtyPurchased



class ShipDeal:
    def __init__(
        self,
        deal_id: UUID,
        seller_id: UUID,
        buyer_id: UUID,
        card_id: UUID,
        qty_purchased: QtyPurchased,
        type_deal: TypeDeal,
        card_created_at: datetime,
        price: Money,
        time_tags: TimeTags,
        deadlines: Deadlines,
        status: StatusDeal
    ) -> None:
        self._deal_id = deal_id
        self._seller_id = seller_id
        self._buyer_id = buyer_id
        self._card_id = card_id
        self._qty_purchased = qty_purchased
        self._type_deal = type_deal
        self._price = price
        self._card_created_at = card_created_at
        self._time_tags = time_tags
        self._deadlines = deadlines
        self._status = status
        self._is_disputed = False

    def confirm_shipment(self, occurred_at: datetime) -> None:
        raise InvalidOperationError()
    
    def delivery_deadline(self) -> datetime:
        return (self._time_tags.created_at
                + self._deadlines.total_shipping_hours)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
                f'deal_id={self._deal_id}, '
                f'seller_id={self._seller_id}, ' 
                f'buyer_id={self._buyer_id}, ' 
                f'card_id={self._card_id}, ' 
                f'qty_purchased={self._qty_purchased}, ' 
                f'type_deal={self._type_deal}, ' 
                f'price={self._price}, ' 
                f'card_created_at={self._card_created_at}, ' 
                f'time_tags={self._time_tags}, ' 
                f'deadlines={self._deadlines}, ' 
                f'status={self._status}, '
                f'is_disputed={self._is_disputed}'
            ')'
        )

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
            .shipped(occurred_at) \
            
        self._status = StatusDeal.AWAITING