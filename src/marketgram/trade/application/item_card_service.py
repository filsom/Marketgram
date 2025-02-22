from datetime import UTC, datetime

from marketgram.common.errors import ApplicationError
from marketgram.common.id_provider import IdProvider
from marketgram.trade.application import commands as cmd
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.description import Description
from marketgram.trade.port.adapter import (
    MembersRepository,
    CardsRepository,
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
        categories_repository: CategoriesRepository,
        id_provider: IdProvider,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self.session = session
        self.id_provider = id_provider
        self.event_dispatcher = event_dispatcher
        self.members_repository = members_repository
        self.cards_repository = cards_repository
        self.categories_repository = categories_repository

    async def create_new_card(self, command: cmd.CreateNewCardCommand) -> None:
        async with self.session.begin():
            category = await self.categories_repository.with_ids(
                command.service_id, command.category_id
            )
            if category is None:
                raise ApplicationError()
            
            seller = await self.members_repository.seller_with_id(
                self.id_provider.user_id()
            )
            seller.can_create_card()
            
            new_card = category.new_card(
                seller.seller_id,
                Description(command.name, command.body),
                Money(command.unit_price),
                command.features,
                command.action_time,
                datetime.now(UTC)
            )
            self.cards_repository.add(new_card)
            await self.session.commit()