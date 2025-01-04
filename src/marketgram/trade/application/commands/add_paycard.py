from dataclasses import dataclass

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.members_repository import (
    MembersRepository
)
from marketgram.trade.domain.model.p2p.paycard import Paycard


@dataclass
class AddPaycardCommand:
    first6: str
    last4: str
    synonym: str


class AddPaycardHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository

    async def handle(self, command: AddPaycardCommand) -> None:
        seller = await self._members_repository \
            .seller_with_id(self._id_provider.provided_id()) 
         
        return seller.change_paycard(
            Paycard(
                command.first6,
                command.last4,
                command.synonym
            )
        )