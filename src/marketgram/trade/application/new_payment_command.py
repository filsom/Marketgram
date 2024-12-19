from dataclasses import dataclass

from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.application.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.p2p.operations_repository import OperationRepository
from marketgram.trade.domain.model.rule.agreement.money import Money


@dataclass
class NewPaymentCommand:
    amount: str


class NewPaymentHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        operations_repository: OperationRepository
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository
        self._operations_repository = operations_repository

    async def handle(self, command: NewPaymentCommand) -> None:
        user = await self._members_repository.user_with_id(
            self._id_provider.provided_id()
        )
        new_payment = user.new_payment(Money(command.amount))
        
        await self._operations_repository.add(new_payment)

        # Запрос в платежную систему