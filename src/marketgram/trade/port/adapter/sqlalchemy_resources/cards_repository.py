from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.card import Card
from marketgram.trade.domain.model.trade_item.sell_card import SellCard


class SQLAlchemyCardsRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def add(self, card: Card) -> None:
        self._async_session.add(card)
    
    async def for_sale_with_price_and_id(
        self,
        price: Money,
        card_id: int
    ) -> SellCard | None:
        stmt = (
            select(SellCard)
            .where(and_(
                SellCard._price == price,
                SellCard._card_id == card_id
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def for_edit_with_owner_and_card_id(
        self,
        owner_id: UUID,
        card_id: int
    ) -> Card | None:
        stmt = (
            select(Card)
            .where(and_(
                SellCard._owner_id == owner_id,
                SellCard._card_id == card_id
            ))
            .with_for_update()
        )
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()