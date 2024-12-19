from dataclasses import dataclass

from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.rule.agreement.money import Money


@dataclass
class NewPaymentCommand:
    amount: str


class NewPaymentHandler:
    def __init__(
        self,
        members_repository: MembersRepository
    ) -> None:
        self._members_repository = members_repository

    async def handle(self, command: NewPaymentCommand) -> None:
        pass 