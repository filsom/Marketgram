from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, text, func

from marketgram.trade.domain.model.p2p_2.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p_2.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p_2.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p_2.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p_2.status_deal import StatusDeal
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.operations_mapper import (
    SQLAlchemyOperationsMapper
)


class SQLAlchemyDealRepository:
    TIME_LIMIT = text("INTERVAL '1' day")

    def __init__(
        self, 
        async_session: AsyncSession,
        operations_mapper: SQLAlchemyOperationsMapper
    ) -> None:
        self._async_session = async_session
        self._operations_mapper = operations_mapper

    async def add(self, deal: ShipDeal) -> None:
        self._async_session.add(deal)

    async def unshipped_with_id(
        self, 
        seller_id: UUID,
        deal_id: UUID
    ) -> ShipDeal | None:
        stmt = (
            select(ShipDeal)
            .where(and_(
                deals_table.c.seller_id == seller_id,
                deals_table.c.deal_id == deal_id,
                deals_table.c.closed_at == None,
                deals_table.c.shipped_at == None,
                deals_table.c.status == StatusDeal.NOT_SHIPPED,
                deals_table.c.created_at + self.TIME_LIMIT > func.now()
            ))
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def unconfirmed_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> ReceiptDeal | None:
        stmt = (
            select(ReceiptDeal)
            .where(and_(
                deals_table.c.buyer_id == buyer_id,
                deals_table.c.deal_id == deal_id,
                deals_table.c.closed_at == None,
                deals_table.c.shipped_at != None,
                deals_table.c.status == StatusDeal.AWAITING,
                deals_table.c.shipped_at + self.TIME_LIMIT > func.now()
            ))
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
                deals_table.c.closed_at == None,
                deals_table.c.status.not_in(
                    [StatusDeal.CANCELLED, 
                    StatusDeal.CLOSED]
                )
            ))
            .with_for_update()
            # .where(and_(
            #     deals_table.c.shipped_at != None,
            #     deals_table.c.shipped_at + self.TIME_LIMIT > func.now()) |
            #     and_(
            #     deals_table.c.created_at + self.TIME_LIMIT > func.now()
            # ))
        )
        result = await self._async_session.execute(stmt)

        return result.scalar()
    
    async def not_disputed_with_id(
        self,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        stmt = (
            select(DisputeDeal)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status != StatusDeal.DISPUTE,
            ))
            .where(or_(
                and_(
                    deals_table.c.closed_at == None, or_(
                    deals_table.c.created_at + self.TIME_LIMIT > func.now(),
                    deals_table.c.shipped_at + self.TIME_LIMIT > func.now()
                )),
                and_(
                    deals_table.c.closed_at != None,
                    deals_table.c.closed_at + self.TIME_LIMIT > func.now()
                )
            ))
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