from dataclasses import dataclass

from marketgram.trade.application.common.exceptions import ApplicationError
from marketgram.trade.application.common.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.p2p.operations_repository import OperationRepository
from marketgram.trade.domain.model.rule.agreement.money import Money


@dataclass
class PayoutCreationCommand:
    amount: str


class PayoutCreationHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        operations_repository: OperationRepository
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository
        self._operations_repository = operations_repository

    async def handle(self, command: PayoutCreationCommand) -> None:
        quantity = await self._operations_repository \
            .quantity_unprocessed_with_seller_id(
                self._id_provider.provided_id()
            )
        if quantity > 0:
            raise ApplicationError()
        
        seller = await self._members_repository \
            .seller_with_balance_and_id(
                self._id_provider.provided_id()
            )
        new_payout = seller.new_payout(Money(command.amount))

        return await self._operations_repository.add(new_payout)