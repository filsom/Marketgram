from enum import StrEnum, auto


class Shipment(StrEnum):
    AUTO = auto()
    HAND = auto()
    CHAT = auto()

    def is_link(self) -> bool:
        return self in [Shipment.AUTO, Shipment.HAND]
    
    def is_not_auto_link(self) -> bool:
        return self in [Shipment.HAND, Shipment.CHAT]

    def is_hand(self) -> bool:
        return self == Shipment.HAND

    def is_auto_link(self) -> bool:
        return self == Shipment.AUTO

    def is_message(self) -> bool:
        return self == Shipment.CHAT
    
    def is_notify_to_the_seller(self) -> bool:
        return self in [Shipment.CHAT, Shipment.HAND]