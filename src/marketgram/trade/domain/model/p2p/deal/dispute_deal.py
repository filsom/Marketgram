from datetime import datetime

from marketgram.trade.domain.model.events import DisputeClosedEvent
from marketgram.trade.domain.model.p2p.errors import QuantityItemError
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import AccountType, Operation


class DisputeDeal:
    def __init__(
        self,
        deal_id: int,
        members: Members,
        unit_price: Money,
        qty_purchased: int,
        deadlines: Deadlines,
        status: StatusDeal,
        entries: list[PostingEntry],
    ) -> None:
        self._deal_id = deal_id
        self._members = members
        self._unit_price = unit_price
        self._qty_purchased = qty_purchased
        self._deadlines = deadlines
        self._entries = entries
        self._status = status
        self.events = []

    def allocate(
        self,
        qty_return: int,
        occurred_at: datetime,
        agreement: ServiceAgreement
    ) -> None:
        if qty_return <= 0:
            raise QuantityItemError()

        if qty_return > self._qty_purchased:
            raise QuantityItemError()

        qty_sell = self._qty_purchased - qty_return

        entry = self._entry_for_buyer(
            qty_return * self._unit_price, 
            occurred_at
        )
        self.entries.append(entry)
    
        if qty_sell:
            self._qty_purchased = qty_sell
            entries = self._entries_for_seller(
                self.amount_deal,
                agreement,
                occurred_at
            )
            self.entries.extend(entries)

        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self.status = StatusDeal.CLOSED

    def close_and_pay_the_seller(
        self, 
        occurred_at: datetime,
        agreement: ServiceAgreement
    ) -> None:
        entries = self._entries_for_seller(
            self.amount_deal,
            agreement,
            occurred_at
        )
        self.entries.extend(entries)
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CLOSED

    def cancel_and_refund(self, occurred_at: datetime) -> None:
        entry = self._entry_for_buyer(
            self.amount_deal, 
            occurred_at
        )
        self.entries.append(entry)
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CANCELLED  

    def _entry_for_buyer(
        self, 
        amount: Money, 
        occurred_at: datetime
    ) -> PostingEntry:
        return PostingEntry(
            self._members.buyer_id,
            amount,
            occurred_at,
            AccountType.USER,
            Operation.REFUND,
            EntryStatus.ACCEPTED
        )

    def _entries_for_seller(
        self, 
        amount: Money,
        agreement: ServiceAgreement,
        occurred_at: datetime
    ) -> list[PostingEntry]:
        temporary_list = []
        temporary_list.append(
            PostingEntry(
                self._members.seller_id,
                agreement.calculate_payment_to_seller(amount),
                occurred_at,
                AccountType.SELLER,
                Operation.SALE,
                EntryStatus.FREEZ
            )
        )
        temporary_list.append(
            PostingEntry(
                agreement.manager_id,
                agreement.calculate_sales_profit(amount),
                occurred_at,
                AccountType.MANAGER,
                Operation.SALE,
                EntryStatus.ACCEPTED
            )
        )
        return temporary_list
    
    @property
    def status(self) -> StatusDeal:
        return self._status
    
    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries
    
    @property
    def amount_deal(self) -> Money:
        return self._qty_purchased * self._unit_price
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DisputeDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)