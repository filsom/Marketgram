from datetime import datetime

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.exceptions import (
    DomainError,
    InvalidOperationError,
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.money import Money


class ShipDeal:
    def __init__(
        self,
        members: Members,
        card_id: int,
        qty_purchased: int,
        type_deal: TypeDeal,
        price: Money,
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
        self._deadlines = deadlines
        self._status = status
        self._is_disputed = is_disputed

    def confirm_shipment(self, occurred_at: datetime) -> None:
        raise InvalidOperationError()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ShipDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)


class ShipLoginCodeDeal(ShipDeal):
    def confirm_shipment(self, occurred_at: datetime) -> None:
        if self._deadlines.shipment < occurred_at:
            raise DomainError()
        
        self._status = StatusDeal.CHECK


class ShipProvidingLinkDeal(ShipDeal):
    def confirm_shipment(self, occurred_at: datetime) -> None:
        if self._deadlines.shipment < occurred_at:
            raise DomainError()
    
        self._status = StatusDeal.AWAITING