from enum import StrEnum, auto


class StatusDispute(StrEnum):
    OPEN = auto()
    PENDING = auto()
    ADMIN_JOINED = auto()
    CLOSED = auto()