from dataclasses import dataclass

from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.application.id_provider import IdProvider
from marketgram.trade.domain.model.p2p.members_repository import (
    MembersRepository
)
from marketgram.trade.domain.model.p2p.paycard import Paycard
from marketgram.trade.domain.model.p2p.seller import Seller


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
        exists_seller = await self._members_repository \
            .seller_with_id(self._id_provider.provided_id()) 
         
        return exists_seller.change_paycard(
            Paycard(
                command.first6,
                command.last4,
                command.synonym
            )
        )