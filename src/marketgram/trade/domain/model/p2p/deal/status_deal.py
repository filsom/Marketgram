from enum import StrEnum, auto


class StatusDeal(StrEnum):
    NOT_SHIPPED = auto()
    INSPECTION = auto()
    CLOSED = auto()
    CANCELLED = auto()
    DISPUTE = auto()
    ADMIN_CLOSED = auto()