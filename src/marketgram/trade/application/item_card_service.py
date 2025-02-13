from datetime import UTC, datetime

from marketgram.common.errors import ApplicationError
from marketgram.common.id_provider import IdProvider
from marketgram.trade.application import commands as cmd
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.description import Description
from marketgram.trade.port.adapter import (
    MembersRepository,
    CardsRepository,
    DealsRepository,
    TradeSession,
    EventDispatcher
)
from marketgram.trade.port.adapter.sqlalchemy_resources.categories_repository import CategoriesRepository


class ItemCardService:
    def __init__(
        self,
        session: TradeSession,
        members_repository: MembersRepository,
        cards_repository: CardsRepository,
        deals_repository: DealsRepository,
        categories_repository: CategoriesRepository,
        id_provider: IdProvider,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._session = session
        self._id_provider = id_provider
        self._event_dispatcher = event_dispatcher
        self._members_repository = members_repository
        self._cards_repository = cards_repository
        self._deals_repository = deals_repository
        self._categories_repository = categories_repository

    async def create_new_card(self, command: cmd.CreateNewCardCommand) -> None:
        async with self._session.begin():
            category = await self._categories_repository.with_ids(
                command.service_id, command.category_id
            )
            if category is None:
                raise ApplicationError()
            
            seller = await self._members_repository.seller_with_id(
                self._id_provider.user_id()
            )
            new_card = category.new_card(
                seller.seller_id,
                Description(command.name, command.body),
                Money(command.unit_price),
                command.features,
                command.action_time,
                datetime.now(UTC)
            )
            self._cards_repository.add(new_card)
            await self._session.commit()

    async def purchase_card(self, command: cmd.CardPurchaseCommand) -> None:
        async with self._session.begin():
            await self._session.trading_lock(
                command.card_id, self._id_provider.user_id()
            )
            card = await self._cards_repository \
                .sell_card_with_id(command.card_id)
            
            if card is None:
                raise ApplicationError()

            buyer = await self._members_repository \
                .user_with_balance_and_id(self._id_provider.user_id())
            
            new_deal = buyer.make_deal(
                command.qty,
                card,
                Money(command.price),
                command.shipment,
                datetime.now(UTC)
            )
            await self._deals_repository.add(new_deal)
            await self._event_dispatcher.dispatch(
                *card.release(), *new_deal.release()
            )
            await self._session.commit()