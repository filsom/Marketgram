from enum import StrEnum, auto


class StatusDeal(StrEnum):
    NOT_SHIPPED = auto()
    AWAITING = auto()
    CHECK = auto()
    CLOSED = auto()
    CANCELLED = auto()
    DISPUTE = auto()