from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.application.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.deal_repository import DealsRepository


@dataclass
class ReceiptConfirmationCommand:
    deal_id: UUID
    occurred_at: datetime


class ReceiptConfirmationHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        deals_repository: DealsRepository
    ) -> None:
        self._id_provider = id_provider
        self._deals_repository = deals_repository

    async def handle(self, command: ReceiptConfirmationCommand) -> None:
        exists_deal = await self._deals_repository \
            .unreceived_with_id(
                self._id_provider.provided_id(),
                command.deal_id
            )
        if exists_deal is None:
            raise ApplicationError()
        
        return exists_deal.confirm_receipt(command.occurred_at)