from marketgram.common.errors import ApplicationError
from marketgram.common.id_provider import IdProvider
from marketgram.trade.port.adapter.event_dispatcher import EventDispatcher
from marketgram.trade.port.adapter.sqlalchemy_resources.agreements_repository import AgreementsRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.deals_repository import DealsRepository
from marketgram.trade.application import commands as cmd
from marketgram.trade.port.adapter.sqlalchemy_resources.disputes_repository import DisputesRepository
from marketgram.trade.port.adapter.sqlalchemy_resources.trade_session import TradeSession


class p2pService:
    def __init__(
        self,
        session: TradeSession,
        id_provider: IdProvider,
        deals_repository: DealsRepository,
        disputes_repository: DisputesRepository,
        agreements_repository: AgreementsRepository,
        event_dispatcher: EventDispatcher
    ) -> None:
        self.session = session
        self.id_provider = id_provider
        self.deals_repository = deals_repository
        self.disputes_repository = disputes_repository
        self.agreements_repository = agreements_repository
        self.event_dispatcher = event_dispatcher

    async def ship(self, command: cmd.ShipCommand) -> None:
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
    
    async def confirm(self, command: cmd.ConfirmCommand) -> None:
        async with self.session.begin():
            await self.session.deal_lock(command.deal_id)
            deal = await self.deals_repository.unconfirmed_with_id(
                self.id_provider.user_id(), command.deal_id
            )
            if deal is None:
                raise ApplicationError()
            
            agreement = await self.agreements_repository.actual()
            deal.confirm(command.occurred_at, agreement)
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

    async def open_dispute(self, command: cmd.CloseCommand) -> None:
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