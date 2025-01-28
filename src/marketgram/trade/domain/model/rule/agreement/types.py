from enum import StrEnum, auto


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


class AccountType(StrEnum):
    USER = auto()
    SELLER = auto()
    TAX = auto()