from dataclasses import dataclass
from enum import StrEnum, auto

from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.money import Money


class ReturnType(StrEnum):
    ITEM = auto()
    MONEY = auto()


@dataclass(frozen=True)
class Claim:
    qty_return: int
    reason: str
    return_type: ReturnType

    def __post_init__(self) -> None:
        if self.qty_return <= 0:
            raise DomainError()
        
    def calculate_amount_return(self, price: Money) -> Money:
        return self.qty_return * price
    
    def return_is_money(self) -> bool:
        return self.return_type == ReturnType.MONEY
    
    def is_replacement(self) -> bool:
        return self.return_type == ReturnType.ITEM 