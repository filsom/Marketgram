from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.p2p.spa.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.spa.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.spa.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.spa.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p.spa.ship_deal import ShipDeal


class DealsRepository(Protocol):
    def add(self, deal: ShipDeal) -> None:
        raise NotImplementedError

    async def unshipped_with_id(
        self, 
        seller_id: UUID,
        deal_id: int
    ) -> ShipDeal | None:
        raise NotImplementedError
    
    async def unreceived_with_id(
        self,
        buyer_id: UUID,
        deal_id: int
    ) -> ReceiptDeal | None:
        raise NotImplementedError

    async def unconfirmed_with_id(
        self,
        buyer_id: UUID,
        deal_id: int
    ) -> ConfirmationDeal | None:
        raise NotImplementedError

    async def unclosed_with_id(
        self,
        seller_id: UUID,
        deal_id: int
    ) -> CancellationDeal | None:
        raise NotImplementedError
    
    async def not_disputed_with_id(
        self,
        buyer_id: UUID,
        deal_id: int
    ) -> DisputeDeal | None:
        raise NotImplementedError
    
    async def disputed_with_id(
        self,
        deal_id: int,
    ) -> DisputeDeal | None:
        raise NotImplementedError