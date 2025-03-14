from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.sell_card import SellCard


class CardsRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def add(self, card) -> None:
        self._async_session.add(card)
    
    async def for_sale_with_price_and_id(
        self,
        price: Money,
        card_id: int
    ) -> SellCard | None:
        stmt = (
            select(SellCard)
            .where(and_(
                SellCard._unit_price == price,
                SellCard._card_id == card_id
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def sell_card_with_id(self, card_id: int) -> SellCard | None:
        stmt = (
            select(SellCard)
            .where(and_(SellCard._card_id == card_id))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()