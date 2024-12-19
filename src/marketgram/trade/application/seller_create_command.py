from dataclasses import dataclass

from marketgram.trade.domain.model.p2p.members_repository import (
    MembersRepository
)


@dataclass
class SellerCreateCommand:
    pass


class SellerCreateHandler:
    def __init__(
        self,
        members_repository: MembersRepository
    ) -> None:
        self._members_repository = members_repository

    async def handle(self, event: SellerCreateCommand) -> None:
        pass