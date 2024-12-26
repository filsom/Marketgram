from dataclasses import dataclass
from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.domain.model.cards_repository import CardsRepository
from marketgram.trade.domain.model.description import AccountFormat, Description, Region
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.p2p.format import Format
from marketgram.trade.domain.model.p2p.members_repository import MembersRepository
from marketgram.trade.domain.model.p2p.transfer_method import TransferMethod
from marketgram.trade.domain.model.rule.agreement.money import Money


@dataclass
class CardCreateCommand:
    amount: str
    title: str
    text_description: str
    account_format: AccountFormat
    region: Region
    spam_block: bool
    format: Format
    method: TransferMethod
    shipping_hours: int | None
    receipt_hours: int | None
    check_hours: int


class CardCreateHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        members_repository: MembersRepository,
        cards_repository: CardsRepository
    ) -> None:
        self._id_provider = id_provider
        self._members_repository = members_repository
        self._cards_repository = cards_repository

    async def handle(self, command: CardCreateCommand) -> None:
        seller = await self._members_repository \
            .seller_with_id(self._id_provider.provided_id())
        
        delivery = Delivery(
            command.format,
            command.method
        )
        new_card = seller.make_card(
            Money(command.amount),
            Description(
                command.title,
                command.text_description,
                command.account_format,
                command.region,
                command.spam_block
            ),
            delivery,
            delivery.calculate_deadlines(
                command.shipping_hours,
                command.receipt_hours,
                command.check_hours
            ) 
        )
        return self._cards_repository.add(new_card)