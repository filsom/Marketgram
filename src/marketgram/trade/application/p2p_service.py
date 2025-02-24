from datetime import UTC, datetime

from marketgram.common.errors import ApplicationError
from marketgram.common.id_provider import IdProvider
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.cards_repository import (
    CardsRepository
)
from marketgram.trade.port.adapter.event_dispatcher import (
    EventDispatcher
)
from marketgram.trade.port.adapter.sqlalchemy_resources.agreements_repository import (
    AgreementsRepository
)
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import (
    DealsRepository
)
from marketgram.trade.application import commands as cmd
from marketgram.trade.port.adapter.sqlalchemy_resources.disputes_repository import (
    DisputesRepository
)
from marketgram.trade.port.adapter.sqlalchemy_resources.members_repository import (
    MembersRepository
)
from marketgram.trade.port.adapter.sqlalchemy_resources.trade_session import TradeSession


class P2PService:
    def __init__(
        self,
        session: TradeSession,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        cards_repository: CardsRepository,
        deals_repository: DealsRepository,
        disputes_repository: DisputesRepository,
        agreements_repository: AgreementsRepository,
        event_dispatcher: EventDispatcher
    ) -> None:
        self.session = session
        self.id_provider = id_provider
        self.members_repository = members_repository
        self.cards_repository = cards_repository
        self.deals_repository = deals_repository
        self.disputes_repository = disputes_repository
        self.agreements_repository = agreements_repository
        self.event_dispatcher = event_dispatcher
        
    async def make_deal(self, command: cmd.CardPurchaseCommand) -> None:
        async with self.session.begin():
            await self.session.trading_lock(
                command.card_id, self.id_provider.user_id()
            )
            card = await self.cards_repository \
                .sell_card_with_id(command.card_id)
            
            if card is None:
                raise ApplicationError()

            buyer = await self.members_repository \
                .user_with_balance_and_id(self.id_provider.user_id())
            
            new_deal = buyer.make_deal(
                command.qty,
                card,
                Money(command.price),
                command.shipment,
                datetime.now(UTC)
            )
            new_deal.notify_seller()

            await self.deals_repository.add(new_deal)
            await self.event_dispatcher.dispatch(
                *card.release_events(), *new_deal.release_events()
            )
            await self.session.commit()

    async def confirm_shipment(self, command: cmd.ShipCommand) -> None:
        async with self.session.begin():
            await self.session.deal_lock(command.deal_id)
            deal = await self.deals_repository.unshipped_with_id(
                self.id_provider.user_id(), command.deal_id
            )
            if deal is None:
                raise ApplicationError()
            
            deal.confirm_shipment(
                command.occurred_at, 
                command.download_link
            )
            await self.event_dispatcher.dispatch(*deal.release_events())
            await self.session.commit()
    
    async def confirm_quality(self, command: cmd.ConfirmCommand) -> None:
        async with self.session.begin():
            await self.session.deal_lock(command.deal_id)
            deal = await self.deals_repository.unconfirmed_with_id(
                self.id_provider.user_id(), command.deal_id
            )
            if deal is None:
                raise ApplicationError()
            
            agreement = await self.agreements_repository.actual()
            deal.confirm_quality(command.occurred_at, agreement)
            await self.session.commit()

    async def open_dispute(self, command: cmd.OpenDisputeCommand) -> None:
        async with self.session.begin():
            await self.session.deal_lock(command.deal_id)
            deal = await self.deals_repository.unconfirmed_with_id(
                self.id_provider.user_id(), command.deal_id
            )
            if deal is None:
                raise ApplicationError()
            
            dispute = deal.open_dispute(
                command.qty_defects,
                command.reason,
                command.return_type,
                command.occurred_at
            )
            await self.disputes_repository.add(dispute)
            await self.event_dispatcher.dispatch(*deal.release_events())
            await self.session.commit()

    async def cancel_failed_trade(self, command: cmd.CancelCommand) -> None:
        async with self.session.begin():
            await self.session.deal_lock(command.deal_id)
            deal = await self.deals_repository.unclosed_with_id(
                self.id_provider.user_id(), command.deal_id
            )
            if deal is None:
                raise ApplicationError()
            
            deal.cancel(command.occurred_at)
            await self.event_dispatcher.dispatch(*deal.release_events())
            await self.session.commit()