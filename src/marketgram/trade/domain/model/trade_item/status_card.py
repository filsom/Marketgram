from enum import StrEnum, auto


class StatusCard(StrEnum):
    EDITING = auto()
    PURCHASED = auto()
    ON_SALE = auto()
    ON_MODERATION = auto()
    REJECTED = auto()