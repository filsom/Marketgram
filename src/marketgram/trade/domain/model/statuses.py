from enum import StrEnum, auto


class StatusCard(StrEnum):
    EDITING = auto()
    PURCHASED = auto()
    ON_SALE = auto()
    ON_FIRST_MODERATION = auto()
    ON_MODERATION = auto()
    REJECTED = auto()


class StatusDeal(StrEnum):
    NOT_SHIPPED = auto()
    INSPECTION = auto()
    CLOSED = auto()
    CANCELLED = auto()
    DISPUTE = auto()
    ADMIN_CLOSED = auto()

    def is_dispute(self) -> bool:
        return self == StatusDeal.DISPUTE
    

class StatusDispute(StrEnum):
    OPEN = auto()
    PENDING = auto()
    ADMIN_JOINED = auto()
    CLOSED = auto()


class StatusDescription(StrEnum):
    NEW = auto()
    CURRENT = auto()
    ARCHIVED = auto()
    CANCELLED = auto()


class EntryStatus(StrEnum):
    FREEZ = auto()
    CANCELLED = auto()
    ACCEPTED = auto()
    TIME_BLOCK = auto()