from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.p2p.payment import Payment
from marketgram.trade.domain.model.p2p.payout import Payout


class OperationRepository(Protocol):
    def add(self, operation: Payment | Payout) -> None:
        raise NotImplementedError

    async def payout_with_seller_id(self, seller_id: UUID) -> Payout | None:
        raise NotImplementedError