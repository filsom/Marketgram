from dataclasses import dataclass
from datetime import UTC, datetime

from marketgram.common.application.acquiring_manager import AcquiringManager
from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.p2p.operations_repository import OperationRepository
from marketgram.trade.domain.model.money import Money


@dataclass
class NewPaymentCreationCommand:
    amount: str


class NewPaymentCreationHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        operations_repository: OperationRepository,
        acquiring_manager: AcquiringManager
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository
        self._operations_repository = operations_repository
        self._acquiring_manager = acquiring_manager

    async def handle(self, command: NewPaymentCreationCommand) -> None:
        user = await self._members_repository.user_with_id(
            self._id_provider.provided_id()
        )
        new_payment = user.new_payment(
            Money(command.amount),
            datetime.now(UTC)
        )
        await self._operations_repository.add(new_payment)

        return self._acquiring_manager.take_payment(new_payment)