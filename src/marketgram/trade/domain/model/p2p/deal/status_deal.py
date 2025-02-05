from enum import StrEnum, auto


class StatusDeal(StrEnum):
    NOT_SHIPPED = auto()
    INSPECTION = auto()
    CLOSED = auto()
    CANCELLED = auto()
    DISPUTE = auto()
    ADMIN_CLOSED = auto()

    def is_not_dispute(self) -> bool:
        return self != StatusDeal.DISPUTE