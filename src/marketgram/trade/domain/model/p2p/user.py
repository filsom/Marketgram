from datetime import datetime
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
from marketgram.trade.domain.model.rule.agreement.entry import EntryStatus, PostingEntry
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.p2p.payment import Payment
from marketgram.trade.domain.model.rule.agreement.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.rule.agreement.types import AccountType, Operation


class User:
    def __init__(self, user_id: UUID) -> None:
        self._user_id = user_id
        self._is_blocked = False
        self._balance: Money = Money(0)
        self._agreement: ServiceAgreement = None
        self._entries: list[PostingEntry] = []

    def make_deal(self, card: SellCard) -> ShipDeal:
        if self._user_id == card.owner_id:
            raise DomainError(BUY_FROM_YOURSELF)

        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)

        remainder = self._balance - card.price
        if remainder < Money(0):
            raise DomainError(INSUFFICIENT_FUNDS)

        self._entries.append(
            PostingEntry(
                self._user_id,
                -card.price,
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
            card.created_in,
            card.price,
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