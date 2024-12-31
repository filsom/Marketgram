from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.trade_item.card import Card
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.sell_card import SellCard


class CardsRepository(Protocol):
    def add(self, card: Card) -> None:
        raise NotImplementedError
    
    async def for_sale_with_price_and_id(
        self,
        price: Money,
        card_id: int
    ) -> SellCard | None:
        raise NotImplementedError
    
    async def for_edit_with_owner_and_card_id(
        self,
        owner_id: UUID,
        card_id: int
    ) -> Card | None:
        raise NotImplementedError