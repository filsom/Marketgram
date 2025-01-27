from dataclasses import dataclass
from uuid import UUID

from marketgram.identity.access.domain.model.errors import DomainError
from marketgram.trade.domain.model.trade_item1.exceptions import BUY_FROM_YOURSELF


@dataclass
class Members:
    seller_id: UUID
    buyer_id: UUID

    def __post_init__(self) -> None:
        if self.seller_id == self.buyer_id:
            raise DomainError(BUY_FROM_YOURSELF)