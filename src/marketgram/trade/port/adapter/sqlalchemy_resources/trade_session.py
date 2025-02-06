from sqlalchemy.ext.asyncio import AsyncSession


class TradeSession(AsyncSession):
    async def trading_lock(self, card_id: int) -> None:
        pass

    async def deal_lock(self, deal_id: int) -> None:
        pass
