from datetime import datetime

from marketgram.trade.domain.model.events import DisputeClosedEvent
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
        qty_sell = self._qty_purchased - qty_return

        self._entries.append(
            PostingEntry(
                self._members.buyer_id,
                qty_return * self._unit_price,
                occurred_at,
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        if qty_sell:
            self._qty_purchased = qty_sell
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
                    agreement._manager_id,
                    agreement.calculate_sales_profit(self.amount_deal),
                    occurred_at,
                    AccountType.MANAGER,
                    Operation.SALE,
                    EntryStatus.ACCEPTED
                )
            )
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
                agreement._manager_id,
                agreement.calculate_sales_profit(self.amount_deal),
                occurred_at,
                AccountType.MANAGER,
                Operation.SALE,
                EntryStatus.ACCEPTED
            )
        )
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CLOSED

    def cancel_and_refund(self, occurred_at: datetime) -> None:
        self._entries.append(
            PostingEntry(
                self._members.buyer_id,
                self.amount_deal,
                occurred_at,
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        self.events.append(
            DisputeClosedEvent(
                self._members.seller_id, 
                occurred_at
            )
        )
        self._status = StatusDeal.CANCELLED  
    
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