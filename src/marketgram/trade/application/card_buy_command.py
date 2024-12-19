from dataclasses import dataclass
from uuid import UUID

from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.application.id_provider import IdProvider
from marketgram.trade.domain.model.cards_repository import CardsRepository
from marketgram.trade.domain.model.p2p.deal_repository import DealsRepository
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.p2p.qty_purchased import QtyPurchased
from marketgram.trade.domain.model.rule.agreement.money import Money


@dataclass
class CardBuyCommand:
    card_id: UUID
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
        exists_card = await self._cards_repository \
            .for_sale_with_price_and_id(
                Money(command.price),
                command.card_id
            )
        if exists_card is None:
            raise ApplicationError()
        
        exists_buyer = await self._members_repository \
            .user_with_balance_and_id(
                self._id_provider.provided_id()
            )
        new_deal = exists_buyer.make_deal(
            QtyPurchased(command.qty),
            exists_card
        )
        return await self._deals_repository.add(new_deal)
