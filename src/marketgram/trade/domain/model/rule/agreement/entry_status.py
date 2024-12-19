from enum import StrEnum, auto


class EntryStatus(StrEnum):
    FREEZ = auto()
    CANCELLED = auto()
    ACCEPTED = auto()
    TIME_BLOCK = auto()