from datetime import datetime
from uuid import UUID, uuid4

from marketgram.common.domain.model.errors import DomainError
from marketgram.trade.domain.model.p2p.paycard import Paycard
from marketgram.trade.domain.model.errors import (
    BALANCE_BLOCKED,
    INSUFFICIENT_FUNDS, 
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.payout import Payout
from marketgram.trade.domain.model.p2p.sales_manager import (
    ServiceAgreement
)


class Seller:
    def __init__(
        self,
        user_id: UUID,
        member_id: int | None = None,
        balance: Money | None = None,
        paycard: Paycard = None,
        is_blocked: bool = False,
    ) -> None:
        self._user_id = user_id
        self._member_id = member_id
        self._paycard = paycard
        self._is_blocked = is_blocked
        self._balance = balance

    def new_payout(
        self, 
        amount: Money,
        agreement: ServiceAgreement,
        current_time: datetime
    ) -> Payout:
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)
        
        if self._paycard is None:
            raise DomainError()
        
        if not agreement.check_amount_payout(amount):
            raise DomainError()

        remainder = self._balance - amount
        if remainder < Money(0):
            raise DomainError(INSUFFICIENT_FUNDS)
        
        return Payout(
            uuid4(),
            self._seller_id,
            self._paycard.synonym,
            amount,
            current_time,
            []
        )
        
    def change_paycard(self, paycard: Paycard) -> None:
        self._paycard = paycard

    @property
    def seller_id(self) -> int:
        return self._member_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Seller):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)