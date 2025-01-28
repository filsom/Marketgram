from dataclasses import dataclass
from enum import StrEnum, auto

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.money import Money


class RegistrationMethod(StrEnum):
    AUTO = auto()
    HAND = auto()


class AccountFormat(StrEnum):
    TDATA = auto()
    TDATA_SESJ = auto()
    SESJ = auto()


class Region(StrEnum):
    RANDOM = auto()
    SNG = auto()
    EUROPE = auto()
    ASIA = auto()
    AMERICA = auto()
    OTHER = auto()


@dataclass
class Description:
    title: str
    body: str

    def __post_init__(self) -> None:
        if len(self.title) < 10:
            raise DomainError()
        
        if len(self.body) < 10:
            raise DomainError()