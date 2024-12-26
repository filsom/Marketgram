from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.application.exceptions import ApplicationError
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
        deal = await self._deals_repository \
            .unreceived_with_id(
                self._id_provider.provided_id(),
                command.deal_id
            )
        if deal is None:
            raise ApplicationError()
        
        return deal.confirm_receipt(command.occurred_at)