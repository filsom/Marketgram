from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.card import Card
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.sell_card import SellCard


class CardsRepository(Protocol):
    def add(self, card: Card) -> None:
        raise NotImplementedError
    
    async def for_sale_with_price_and_id(
        self,
        price: Money,
        card_id: UUID
    ) -> SellCard | None:
        raise NotImplementedError