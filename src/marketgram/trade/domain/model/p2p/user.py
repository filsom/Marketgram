from datetime import datetime
from uuid import UUID, uuid4

from marketgram.trade.domain.model.p2p.sales_manager import ServiceAgreement
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.exceptions import (
    BALANCE_BLOCKED,
    INSUFFICIENT_FUNDS,
    MINIMUM_DEPOSIT, 
    DomainError
)
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.posting_entry import EntryStatus, PostingEntry
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.payment import Payment
from marketgram.trade.domain.model.types import AccountType, Operation



class User:
    def __init__(
        self, 
        user_id: UUID,
        entries: list[PostingEntry],
        balance: Money | None = None,
        member_id: int | None = None,
        is_blocked: bool = False
    ) -> None:
        self._user_id = user_id
        self._member_id = member_id
        self._is_blocked = is_blocked
        self._balance = balance
        self._entries = entries

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

        deal = card.purchase(self._user_id, quantity, current_time)

        self._entries.append(
            PostingEntry(
                self._member_id,
                deal.write_off_ammount,
                current_time,
                AccountType.USER,
                Operation.BUY,
                EntryStatus.ACCEPTED
            )
        )
        return deal

    def new_payment(
        self, 
        amount: Money,
        agreement: ServiceAgreement,
        current_time: datetime
    ) -> Payment:  
        if self._is_blocked:
            raise DomainError(BALANCE_BLOCKED)
        
        if not amount < agreement.check_amount_payment(amount):
            raise DomainError(MINIMUM_DEPOSIT)

        return Payment(
            uuid4(),
            self._member_id,
            amount,
            current_time,
        )
    
    @property
    def buyer_id(self) -> int:
        return self._member_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)