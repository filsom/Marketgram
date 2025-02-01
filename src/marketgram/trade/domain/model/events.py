from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal


@dataclass(frozen=True)
class DisputeOpenedEvent:
    seller_id: UUID
    occurred_at: datetime


@dataclass(frozen=True)
class DisputeClosedEvent:
    seller_id: UUID
    occurred_at: datetime


@dataclass(frozen=True)
class PurchasedCardWithAutoShipmentEvent:
    deal: ShipDeal
    occurred_at: datetime


@dataclass(frozen=True)
class PurchasedCardWithHandProvidingNotification:
    seller_id: UUID
    deal_id: int
    qty: int
    shipped_at: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedByDealNotification:
    buyer_id: UUID
    deal_id: int
    download_link: str
    occurred_at: datetime