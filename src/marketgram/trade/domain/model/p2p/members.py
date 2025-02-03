from dataclasses import dataclass
from uuid import UUID

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.exceptions import BUY_FROM_YOURSELF


@dataclass
class Members:
    seller_id: int
    buyer_id: int

    def __post_init__(self) -> None:
        if self.seller_id == self.buyer_id:
            raise DomainError(BUY_FROM_YOURSELF)