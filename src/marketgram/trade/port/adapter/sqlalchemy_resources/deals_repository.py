from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from sqlalchemy.orm import with_polymorphic

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.deal.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.operations_mapper import (
    SQLAlchemyOperationsMapper
)


class SQLAlchemyDealsRepository:
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
        deal_id: int
    ) -> ShipDeal | None:
        ship_deal = with_polymorphic(ShipDeal, '*')
        stmt = (
            select(ship_deal)
            .join(Members, Members.seller_id == seller_id)
            .where(and_(
                ship_deal._deal_id == deal_id,
                ship_deal._status == StatusDeal.NOT_SHIPPED,
            ))
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar()
    
    async def unconfirmed_with_id(
        self,
        buyer_id: UUID,
        deal_id: int
    ) -> ConfirmationDeal | None:
        stmt = (
            select(ConfirmationDeal)
            .join(Members, Members.buyer_id == buyer_id)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.INSPECTION,
            ))
        )
        result = await self._async_session.execute(stmt)
        
        return result.scalar()
    
    async def unclosed_with_id(
        self,
        seller_id: UUID,
        deal_id: int
    ) -> CancellationDeal | None:
        stmt = (
            select(CancellationDeal)
            .join(Members, Members.seller_id == seller_id)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status.not_in([
                    StatusDeal.CANCELLED, 
                    StatusDeal.CLOSED
                ])
            ))
        )
        result = await self._async_session.execute(stmt)

        return result.scalar()
    
    async def not_disputed_with_id(
        self,
        buyer_id: UUID,
        deal_id: int,
    ) -> DisputeDeal | None:
        stmt = (
            select(DisputeDeal)
            .join(Members, Members.buyer_id == buyer_id)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.INSPECTION,
            ))
        )
        result = await self._async_session.execute(stmt)

        return result.scalar()

    async def disputed_with_id(
        self,
        deal_id: int,
    ) -> DisputeDeal | None:
        stmt = (
            select(DisputeDeal)
            .join(Members)
            .where(and_(
                deals_table.c.deal_id == deal_id,
                deals_table.c.status == StatusDeal.DISPUTE,
            ))
        )
        result = await self._async_session.execute(stmt)

        return result.scalar()