from enum import StrEnum, auto


INFINITY = 'infinity'


class EventType(StrEnum):
    PRODUCT_CONFIRMED = auto()
    USER_DEDUCED = auto()
    TAX_PAYMENT = auto()
    TAX_PAYOUT = auto()


class Operation(StrEnum):
    TAX = auto()
    BUY = auto()
    DEPOSIT = auto()
    REFUND = auto()
    SALE = auto()
    PAYOUT = auto()
    PAYMENT = auto()


class AccountType(StrEnum):
    USER = auto()
    SELLER = auto()
    MANAGER = auto()


class InventoryOperation(StrEnum):
    UPLOADING = auto()
    BUY = auto()