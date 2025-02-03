from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.deal.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.deals_table import (
    deals_entries_table,
    deals_members_table,
    deals_table
)
from tests.integration.trade.conftest import BUYER, MANAGER, SELLER


@dataclass(frozen=True)
class Deal:
    unshipped: ShipDeal | None
    unconfirmed: ConfirmationDeal | None
    unclosed: CancellationDeal | None
    not_disputed: DisputeDeal | None
    disputed: DisputeDeal | None


class TradeTestCase:
    @pytest.fixture(autouse=True)
    def _set_async_engine(
        self, 
        engine: AsyncGenerator[AsyncEngine, None]
    ) -> None:
        self._engine = engine

    async def query_deal_id(self) -> int:
        async with AsyncSession(self._engine) as session:
            stmt = select(ShipDeal)
            result = await session.execute(stmt)
            deal_id = result.scalar().deal_id
            return deal_id

    async def query_multiple_deal_statuses(self) -> Deal:
        async with AsyncSession(self._engine) as session:
            deal_id = await self.query_deal_id()
            deals_repository = DealsRepository(session)

            unshipped_deal  = await deals_repository.unshipped_with_id(SELLER[1], deal_id)
            unconfirmed_deal = await deals_repository.unconfirmed_with_id(BUYER[1], deal_id)
            unclosed_deal = await deals_repository.unclosed_with_id(SELLER[1], deal_id)
            not_disputed_deal = await deals_repository.not_disputed_with_id(BUYER[1], deal_id)
            disputed_deal = await deals_repository.disputed_with_id(deal_id)

            return Deal(
                unshipped_deal,
                unconfirmed_deal,
                unclosed_deal,
                not_disputed_deal,
                disputed_deal
            )

    async def delete_deal(self) -> None:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            for table in [deals_table, deals_members_table, deals_entries_table]:
                stmt = delete(table)
                await session.execute(stmt)
                await session.commit()

    def make_service_agreement(self) -> ServiceAgreement:
        return ServiceAgreement(
            MANAGER[1],
            Decimal('0.1'),
            Decimal('0.1'),
            Money(100),
            Money(100),
            datetime.now(UTC),
        )