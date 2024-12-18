from dataclasses import dataclass

from marketgram.trade.domain.model.exceptions import DomainError


@dataclass(frozen=True)
class QtyPurchased:
    total: int

    def __post_init__(self) -> None:
        if not isinstance(self.total, int):
            raise DomainError()
        
        if self.total <= 0:
            raise DomainError()