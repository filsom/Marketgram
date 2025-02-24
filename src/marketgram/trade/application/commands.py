from dataclasses import dataclass
from datetime import datetime

from marketgram.trade.domain.model.p2p.claim import ReturnType
from marketgram.trade.domain.model.p2p.shipment import Shipment


@dataclass
class CardPurchaseCommand:
    card_id: int
    qty: int
    price: str
    shipment: Shipment


@dataclass
class CreateNewCardCommand:
    service_id: int
    category_id: int
    name: str
    body: str
    unit_price: str
    features: dict[str, str] | None
    action_time: dict[str, int] | None 


@dataclass
class ShipCommand:
    deal_id: int
    occurred_at: datetime
    download_link: str | None = None


@dataclass
class ConfirmCommand:
    deal_id: int
    occurred_at: datetime


@dataclass
class CancelCommand:
    deal_id: int
    occurred_at: datetime


@dataclass
class OpenDisputeCommand:
    deal_id: int
    qty_defects: int
    reason: str
    return_type: ReturnType
    occurred_at: datetime