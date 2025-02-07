from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


class TradeSession(AsyncSession):
    async def trading_lock(self, card_id: int, user_id: UUID) -> None:
        pass

    async def deal_lock(self, deal_id: int) -> None:
        pass

    async def card_lock(self, card_id: int) -> None:
        pass
