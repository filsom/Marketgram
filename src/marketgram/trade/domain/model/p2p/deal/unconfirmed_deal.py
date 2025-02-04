from datetime import datetime
from uuid import uuid4

from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.events import DisputeOpenedNotification
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deal.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.deal.dispute import Dispute
from marketgram.trade.domain.model.p2p.errors import (
    DO_NOT_OPEN_DISPUTE, 
    LATE_CONFIRMATION, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.sales_manager import ServiceAgreement
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.types import AccountType, Operation


class UnconfirmedDeal:
    def __init__(
        self, 
        deal_id: int,
        members: Members,
        price: Money,
        qty_purcased: int,
        deadlines: Deadlines,
        status: StatusDeal,
        inspected_at: datetime | None,
        entries: list[PostingEntry]
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._price = price
        self._qty_purchased = qty_purcased
        self._deadlines = deadlines
        self._status = status
        self._inspected_at = inspected_at
        self._entries = entries
        self.events = []

    def confirm(self, occurred_at: datetime, agreement: ServiceAgreement) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise CheckDeadlineError(LATE_CONFIRMATION)

        self._entries.append(
            PostingEntry(
                self._members.seller_id,
                agreement.calculate_payment_to_seller(self.amount_deal),
                occurred_at,
                AccountType.SELLER,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        self._entries.append(
            PostingEntry(
                agreement.manager_id,
                agreement.calculate_sales_profit(self.amount_deal),
                occurred_at,
                AccountType.MANAGER,
                Operation.SALE,
                EntryStatus.ACCEPTED
            )
        )
        self._inspected_at = occurred_at
        self._status = StatusDeal.CLOSED
        
    def open_dispute(
        self, 
        qty_defects: int, 
        reason: str, 
        return_type: ReturnType, 
        occurred_at: datetime
    ) -> Dispute:   
        if not self._deadlines.check(self._status, occurred_at):
            raise CheckDeadlineError(DO_NOT_OPEN_DISPUTE)
        
        if qty_defects > self._qty_purchased:
            raise DomainError()

        self._status = StatusDeal.DISPUTE
        self.events.append(
            DisputeOpenedNotification(
                self._members.seller_id, 
                occurred_at
            )
        )        
        return Dispute(
            uuid4(),
            Claim(qty_defects, reason, return_type),
            self._members.start_dispute(self._deal_id),
            self._price,
            occurred_at
        )

    @property
    def status(self) -> StatusDeal:
        return self._status
    
    @property
    def inspected_at(self) -> datetime:
        return self._inspected_at
    
    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries
    
    @property
    def amount_deal(self) -> Money:
        return self._price * self._qty_purchased

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnconfirmedDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)