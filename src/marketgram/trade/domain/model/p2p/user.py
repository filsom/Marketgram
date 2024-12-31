from datetime import datetime
from uuid import UUID, uuid4

from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.trade_item.exceptions import (
    BALANCE_BLOCKED,
    INSUFFICIENT_FUNDS,
    MINIMUM_DEPOSIT, 
    DomainError
)
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.p2p.spa.ship_deal import ShipDeal
from marketgram.trade.domain.model.rule.agreement.entry import (
    EntryStatus, 
    Entry
)
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.p2p.payment import Payment
from marketgram.trade.domain.model.rule.agreement.service_agreement import (
    ServiceAgreement
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    Operation
)


class User:
    def __init__(
        self, 
        user_id: UUID,
        is_blocked: bool = False,
        balance: Money = Money(0)
    ) -> None:
        self._user_id = user_id
        self._is_blocked = is_blocked
        self._balance = balance
        self._entries: list[Entry] = []
        self._agreement: ServiceAgreement = None

    def make_deal(
        self, 
        quantity: int, 
        card: SellCard,
        current_time: datetime
    ) -> ShipDeal:
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        remainder = self._balance - card.price * quantity
        if remainder < Money(0):
            raise DomainError(INSUFFICIENT_FUNDS)

        card.buy(quantity)

        self._entries.append(
            Entry(
                self._user_id,
                -card.price * quantity,
                current_time,
                AccountType.USER,
                Operation.BUY,
                EntryStatus.ACCEPTED
            )
        )
        return ShipDeal(
            Members(
                card.owner_id,
                self._user_id
            ),
            card.card_id,
            card.type_deal,
            card.created_in,
            card.price * quantity,
            card.time_tags(current_time),
            card.deadlines,
            card.status_deal
        )  

    def new_payment(
        self, 
        amount: Money,
        current_time: datetime
    ) -> Payment:  
        limits = self._agreement.actual_limits()
        
        if amount < limits.min_deposit:
            raise DomainError(MINIMUM_DEPOSIT)
        
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        return Payment(
            uuid4(),
            self._user_id,
            amount,
            current_time,
        )

    def accept_agreement(self, agreement: ServiceAgreement) -> None:
        self._agreement = agreement

    def __eq__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)