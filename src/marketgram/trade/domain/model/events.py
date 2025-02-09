from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
    from marketgram.trade.domain.model.p2p.deal.opened_dispute import OpenedDispute
    from marketgram.trade.domain.model.p2p.deal.admin_dispute import AdminDispute


# Разблокировать выплату продавцу.
@dataclass(frozen=True)
class DisputeClosedEvent:
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class PurchasedCardWithAutoShipmentEvent:
    deal: ShipDeal
    occurred_at: datetime


# Покупатель закрывает спор. Перевести полную оплату продавцу.
@dataclass(frozen=True)
class BuyerClosedDisputeEvent:
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerShippedReplacementWithAutoShipmentEvent:
    dispute: OpenedDispute
    qty_return: int
    occurred_at: datetime


# Участики дождались админа и по его решению была произведена замена.
@dataclass(frozen=True)
class AdminShippedReplacementWithAutoShipmentEvent:
    dispute: AdminDispute
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести частичную оплату продавцу.
@dataclass(frozen=True)
class SellerClosedDisputeWithRefundEvent:
    deal_id: int
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести частичную оплату продавцу.
@dataclass(frozen=True)
class AdminClosedDisputeWithRefundEvent:
    deal_id: int
    qty_return: int
    occurred_at: datetime


# Закрыть сделку и перевести полную оплату продавцу.
@dataclass(frozen=True)
class BuyerConfirmedAndClosedDisputeEvent:
    deal_id: int
    occurred_at: datetime