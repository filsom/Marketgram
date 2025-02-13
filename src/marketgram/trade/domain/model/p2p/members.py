from dataclasses import dataclass

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.errors import BUY_FROM_YOURSELF


@dataclass(frozen=True)
class DisputeMembers:
    deal_id: int
    seller_id: int
    buyer_id: int


@dataclass(frozen=True)
class Members:
    seller_id: int
    buyer_id: int

    def __post_init__(self) -> None:
        if self.seller_id == self.buyer_id:
            raise DomainError(BUY_FROM_YOURSELF)
        
    def start_dispute(self, deal_id: int) -> DisputeMembers:
        return DisputeMembers(
            deal_id,
            self.seller_id,
            self.buyer_id
        )