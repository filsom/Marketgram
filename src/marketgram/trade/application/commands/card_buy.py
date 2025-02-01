from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.domain.model.trade_item1.cards_repository import CardsRepository
from marketgram.trade.domain.model.p2p.deal.deal_repository import DealsRepository
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.money import Money


@dataclass
class CardBuyCommand:
    card_id: int
    qty: int
    price: str


class CardBuyHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        cards_repository: CardsRepository,
        deals_repository: DealsRepository,
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository
        self._cards_repository = cards_repository
        self._deals_repository = deals_repository

    async def handle(self, command: CardBuyCommand) -> None:
        card = await self._cards_repository \
            .for_sale_with_price_and_id(
                Money(command.price),
                command.card_id
            )
        if card is None:
            raise ApplicationError()
        
        buyer = await self._members_repository \
            .user_with_balance_and_id(
                self._id_provider.provided_id()
            )
        new_deal = buyer.make_deal(
            command.qty,
            card,
            datetime.now(UTC)
        )
        return await self._deals_repository.add(new_deal)
