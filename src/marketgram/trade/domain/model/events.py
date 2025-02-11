from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from marketgram.common.entity import DomainEvent

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
    from marketgram.trade.domain.model.p2p.deal.opened_dispute import OpenedDispute
    from marketgram.trade.domain.model.p2p.deal.admin_dispute import AdminDispute


# Разблокировать выплату продавцу.
@dataclass(frozen=True)
class DisputeClosedEvent(DomainEvent):
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class PurchasedCardWithAutoShipmentEvent(DomainEvent):
    deal: ShipDeal
    occurred_at: datetime


# Покупатель закрывает спор. Перевести полную оплату продавцу.
@dataclass(frozen=True)
class BuyerClosedDisputeEvent(DomainEvent):
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerShippedReplacementWithAutoShipmentEvent(DomainEvent):
    dispute: OpenedDispute
    qty_return: int
    occurred_at: datetime


# Участики дождались админа и по его решению была произведена замена.
@dataclass(frozen=True)
class AdminShippedReplacementWithAutoShipmentEvent(DomainEvent):
    dispute: AdminDispute
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести частичную оплату продавцу.
@dataclass(frozen=True)
class SellerClosedDisputeWithRefundEvent(DomainEvent):
    deal_id: int
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести частичную оплату продавцу.
@dataclass(frozen=True)
class AdminClosedDisputeWithRefundEvent(DomainEvent):
    deal_id: int
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести полную оплату продавцу.
@dataclass(frozen=True)
class BuyerConfirmedAndClosedDisputeEvent(DomainEvent):
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerShippedItemManuallyEvent(DomainEvent):
    deal_id: int
    download_link: str
    occurred_at: datetime