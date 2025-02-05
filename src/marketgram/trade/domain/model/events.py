from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal


@dataclass(frozen=True)
class DisputeOpenedNotification:
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class DisputeClosedEvent:
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class PurchasedCardWithAutoShipmentEvent:
    deal: ShipDeal
    occurred_at: datetime


@dataclass(frozen=True)
class DealCreatedNotification:
    seller_id: int
    deal_id: int
    card_id: int
    qty: int
    shipped_at: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedByDealNotification:
    buyer_id: int
    deal_id: int
    download_link: str
    occurred_at: datetime


@dataclass(frozen=True)
class ZeroInventoryBalanceNotification:
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerCancelledDealNotification:
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerCancelledDisputeDealEvent:
    deal_id: int
    qty_return: int
    occurred_at: datetime


@dataclass(frozen=True)
class DefectiveItemShipped:
    pass


@dataclass(frozen=True)
class ReissuePurchasedCardNotification:
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class BuyerClosedDisputeEvent:
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerClosedDisputeWithAutoShipmentEvent:
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class AdminJoinNotification:
    deal_id: int
    occurred_at: datetime