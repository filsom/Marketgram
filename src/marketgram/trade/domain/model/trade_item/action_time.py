from dataclasses import dataclass

from marketgram.common.application.exceptions import DomainError


@dataclass
class ActionTime:
    shipping_hours: int | None
    receipt_hours: int | None
    inspection_hours: int

    def __post_init__(self) -> None:
        for key in self.__dict__:
            if self.__dict__[key] is not None and self.__dict__[key] < 1:
                raise DomainError()