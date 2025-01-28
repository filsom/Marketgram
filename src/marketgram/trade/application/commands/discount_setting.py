from dataclasses import dataclass
from uuid import UUID

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.domain.model.trade_item1.cards_repository import CardsRepository
from marketgram.trade.domain.model.money import Money


@dataclass
class DiscountSettingCommand:
    card_id: int
    amount: str


class DiscountSettingHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        cards_repository: CardsRepository
    ) -> None:
        self._id_provider = id_provider
        self._cards_repository = cards_repository

    async def handle(self, command: DiscountSettingCommand) -> None:
        card = await self._cards_repository \
            .for_edit_with_owner_and_card_id(
                self._id_provider.provided_id(),
                command.card_id
            )
        if card is None:
            raise ApplicationError()
        
        return card.set_discounted_price(Money(command.amount))