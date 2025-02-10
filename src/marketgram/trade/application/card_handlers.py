from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.port.adapter.id_provider import IDProvider
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.port.adapter.event_dispatcher import EventDispatcher
from marketgram.trade.port.adapter.sqlalchemy_resources.cards_repository import CardsRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.members_repository import MembersRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.trade_session import TradeSession


@dataclass
class CardBuyCommand:
    card_id: int
    qty: int
    price: str
    shipment: Shipment


class CardBuyHandler:
    def __init__(
        self,
        session: TradeSession,
        id_provider: IDProvider,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._session = session
        self._id_provider = id_provider
        self._event_dispatcher = event_dispatcher
        self._members_repository = MembersRepository(session)
        self._cards_repository = CardsRepository(session)
        self._deals_repository = DealsRepository(session)

    async def handle(self, command: CardBuyCommand) -> None:
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