from enum import StrEnum, auto


INFINITY = 'infinity'


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