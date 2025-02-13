from typing import Protocol
from marketgram.trade.domain.model.trade_item.sell_card import SellCard


class CardsRepository(Protocol):
    async def sell_card_with_id(self, card_id: int) -> SellCard:
        raise NotImplementedError