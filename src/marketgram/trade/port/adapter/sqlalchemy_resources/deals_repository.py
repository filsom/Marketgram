from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, text
from sqlalchemy.orm import with_polymorphic

from marketgram.trade.domain.model.p2p.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.operations_mapper import (
    SQLAlchemyOperationsMapper
)


class SQLAlchemyDealRepository:
    def __init__(
        self, 
        async_session: AsyncSession,
        operations_mapper: SQLAlchemyOperationsMapper
    ) -> None:
        self._async_session = async_session
        self._operations_mapper = operations_mapper

    def add(self, deal: ShipDeal) -> None:
        self._async_session.add(deal)

    async def unshipped_with_id(
        self, 
        seller_id: UUID,
        deal_id: UUID
    ) -> ShipDeal | None:
        ship_deal = with_polymorphic(ShipDeal, '*')
        stmt = (
            select(ship_deal)
            .where(and_(
                ship_deal._seller_id == seller_id,
                ship_deal._deal_id == deal_id,
                ship_deal._status == StatusDeal.NOT_SHIPPED,
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def unreceived_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> ReceiptDeal | None:
        stmt = (
            select(ReceiptDeal)
            .where(and_(
                deals_table.c.buyer_id == buyer_id,
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.AWAITING,
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def unconfirmed_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> ConfirmationDeal | None:
        stmt = (
            select(ConfirmationDeal)
            .where(and_(
                deals_table.c.buyer_id == buyer_id,
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.CHECK,
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def unclosed_with_id(
        self,
        seller_id: UUID,
        deal_id: UUID
    ) -> CancellationDeal | None:
        stmt = (
            select(CancellationDeal)
            .where(and_(
                deals_table.c.seller_id == seller_id,
                deals_table.c.deal_id == deal_id,
                deals_table.c.status.not_in([
                    StatusDeal.CANCELLED, 
                    StatusDeal.CLOSED
                ])
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar()
    
    async def not_disputed_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        stmt = (
            select(DisputeDeal)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.buyer_id == buyer_id,
                deals_table.c.status.not_in([
                    StatusDeal.DISPUTE,
                    StatusDeal.CLOSED,
                    StatusDeal.CANCELLED
                ]),
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        deal = result.scalar()
        if deal is None:
            return None
        
        payout = await self._operations_mapper \
            .payout_with_seller_id(deal._seller_id)
        
        deal._add_payout(payout)

        return deal

    async def disputed_with_id(
        self,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        stmt = (
            select(DisputeDeal)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.DISPUTE,
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        deal = result.scalar()
        if deal is None:
            return None
        
        payout = await self._operations_mapper \
            .payout_with_seller_id(deal._seller_id)
        
        deal._add_payout(payout)

        return deal