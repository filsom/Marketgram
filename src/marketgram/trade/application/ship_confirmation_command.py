from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.domain.model.p2p.deal_repository import DealsRepository


@dataclass
class ShipConfirmationCommand:
    deal_id: UUID


class ShipConfirmationHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        deals_repository: DealsRepository
    ) -> None:
        self._id_provider = id_provider
        self._deals_repository = deals_repository

    async def handle(self, command: ShipConfirmationCommand) -> None:
        deal = await self._deals_repository \
            .unshipped_with_id(
                self._id_provider.provided_id(),
                command.deal_id
            )
        if deal is None:
            raise ApplicationError()
        
        return deal.confirm_shipment(datetime.now(UTC))