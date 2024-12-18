from datetime import datetime
from uuid import UUID, uuid4

from marketgram.trade.domain.model.card import Card
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.p2p.paycard import Paycard
from marketgram.trade.domain.model.rule.agreement.service_agreement import (
    ServiceAgreement
)
from marketgram.trade.domain.model.exceptions import (
    BALANCE_BLOCKED,
    INSUFFICIENT_FUNDS, 
    MINIMUM_PRICE, 
    MINIMUM_WITHDRAW,
    DomainError
)
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.description import Description
from marketgram.trade.domain.model.p2p.payout import Payout


class Seller:
    def __init__(
        self, 
        user_id: UUID
    ) -> None:
        self._user_id = user_id
        self._paycard: Paycard = None
        self._is_blocked = False
        self._balance: Money = Money(0)
        self._agreement: ServiceAgreement = None

    def make_card(
        self, 
        amount: Money, 
        description: Description,
        delivery: Delivery,
        deadlines: Deadlines | None
    ) -> Card:
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)
        
        limits = self._agreement.actual_limits()

        if amount < limits.min_price:
            raise DomainError(MINIMUM_PRICE)

        if deadlines is None:
            deadlines = self._agreement.default_deadlines()

        return Card(
            uuid4(),
            self._user_id,
            amount,
            description,
            delivery,
            deadlines,
            limits.min_price,
            limits.min_discount,
            datetime.now()
        )

    def new_payout(self, amount: Money) -> Payout:
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        limits = self._agreement.actual_limits()
        
        if amount < limits.min_withdraw:
            raise DomainError(MINIMUM_WITHDRAW)

        remainder = self._balance - amount
        if remainder < Money(0):
            raise DomainError(INSUFFICIENT_FUNDS)
        
        return Payout(
            uuid4(),
            self._user_id,
            self._paycard.synonym,
            amount,
            datetime.now(),
        )
        
    def change_paycard(self, paycard: Paycard) -> None:
        self._paycard = paycard

    def accept_agreement(self, agreement: ServiceAgreement) -> None:
        self._agreement = agreement

    def __eq__(self, other: 'Seller') -> bool:
        if not isinstance(other, Seller):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)