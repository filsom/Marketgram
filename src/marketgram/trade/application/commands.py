from dataclasses import dataclass

from marketgram.trade.domain.model.p2p.deal.shipment import Shipment


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
    features: dict[str, str]
    action_time: dict[str, int] | None 