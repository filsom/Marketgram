from dataclasses import dataclass

from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.domain.model.p2p.members_repository import (
    MembersRepository
)
from marketgram.trade.domain.model.p2p.paycard import Paycard
from marketgram.trade.domain.model.p2p.seller import Seller


@dataclass
class SellerCreateCommand:
    first6: str
    last4: str
    synonym: str


class SellerCreateHandler:
    def __init__(
        self,
        members_repository: MembersRepository
    ) -> None:
        self._members_repository = members_repository

    async def handle(self, command: SellerCreateCommand) -> None:
        exists_seller = await self._members_repository \
            .seller_with_id(...) 
        
        if exists_seller:
            raise ApplicationError()
        
        new_seller = Seller(
            self._members_repository.next_identity(),
            Paycard(
                command.first6,
                command.last4,
                command.synonym
            )
        )
        return self._members_repository.add(new_seller)