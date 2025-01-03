from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.trade.domain.model.p2p.payout import Payout


class SQLAlchemyOperationsMapper:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def add(self, payout: Payout) -> None:
        self._async_session.add(payout)

    async def payout_with_seller_id(self, seller_id: UUID) -> Payout | None:
        stmt = (
            select(Payout)
            .where(and_(
                Payout._user_id == seller_id,
                Payout._is_processed == False
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()