from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from marketgram.trade.domain.model.exceptions import (
    BALANCE_BLOCKED,
    BUY_FROM_YOURSELF, 
    INSUFFICIENT_FUNDS,
    MINIMUM_DEPOSIT, 
    DomainError
)
from marketgram.trade.domain.model.sell_card import SellCard
from marketgram.trade.domain.model.p2p.ship_deal import ShipDeal
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

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.qty_purchased import QtyPurchased


class User:
    def __init__(
        self, 
        user_id: UUID,
        entries: list[Entry],
        is_blocked: bool = False,
        balance: Money = Money(0)
    ) -> None:
        self._user_id = user_id
        self._entries = entries
        self._is_blocked = is_blocked
        self._balance = balance
        self._agreement: ServiceAgreement = None

    def make_deal(self, qty: QtyPurchased, card: SellCard) -> ShipDeal:
        if self._user_id == card.owner_id:
            raise DomainError(BUY_FROM_YOURSELF)

        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        remainder = self._balance - card.price
        if remainder < Money(0):
            raise DomainError(INSUFFICIENT_FUNDS)

        self._entries.append(
            Entry(
                self._user_id,
                -card.price * qty,
                datetime.now(),
                AccountType.USER,
                Operation.BUY,
                EntryStatus.ACCEPTED
            )
        )
        card.buy()

        return ShipDeal(
            uuid4(),
            card.owner_id,
            self._user_id,
            card.card_id,
            card.type_deal,
            card.created_in,
            card.price * qty,
            card.time_tags(datetime.now()),
            card.deadlines,
            card.status_deal
        )  

    def new_payment(self, amount: Money) -> Payment:  
        limits = self._agreement.actual_limits()
        
        if amount < limits.min_deposit:
            raise DomainError(MINIMUM_DEPOSIT)
        
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        return Payment(
            uuid4(),
            self._user_id,
            amount,
            datetime.now(),
        )

    def accept_agreement(self, agreement: ServiceAgreement) -> None:
        self._agreement = agreement

    def __eq__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)