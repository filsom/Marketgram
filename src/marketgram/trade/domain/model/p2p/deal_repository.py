from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.p2p_2.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p_2.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p_2.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p_2.ship_deal import ShipDeal


class DealRepository(Protocol):
    async def add(self, deal: ShipDeal) -> None:
        raise NotImplementedError

    async def unshipped_with_id(
        self, 
        deal_id: UUID, 
        seller_id: UUID
    ) -> ShipDeal | None:
        raise NotImplementedError

    async def unconfirmed_with_id(
        self,
        deal_id: UUID,
        buyer_id: UUID
    ) -> ReceiptDeal | None:
        raise NotImplementedError

    async def unclosed_with_id(
        self,
        deal_id: UUID,
        seller_id: UUID
    ) -> CancellationDeal | None:
        raise NotImplementedError
    
    async def not_disputed_with_id(
        self,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        raise NotImplementedError
    
    async def disputed_with_id(
        self,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        raise NotImplementedError
