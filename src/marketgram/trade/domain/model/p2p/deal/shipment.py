from enum import StrEnum, auto


class Shipment(StrEnum):
    AUTO = auto()
    HAND = auto()
    CHAT = auto()

    def is_link(self) -> bool:
        return self in [Shipment.AUTO, Shipment.HAND]

    def is_message(self) -> bool:
        return self in Shipment.CHAT