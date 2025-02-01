from datetime import datetime

from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.types import AccountType, Operation


class OverdueDeal:
    def __init__(
        self, 
        deal_id: int,
        members: Members,
        price: Money,
        qty_purchased: int,
        status: StatusDeal,
        entries: list[PostingEntry]
    ):
        self._deal_id = deal_id
        self._members = members
        self._price = price
        self._qty_purchased = qty_purchased
        self._status = status
        self._entries = entries

    def cancel(
        self, 
        occurred_at: datetime, 
        agreement: ServiceAgreement
    ) -> None:
        match self._status:
            case StatusDeal.NOT_SHIPPED:
                self._entries.append(
                    PostingEntry(
                        self._members.buyer_id,
                        self._price,
                        occurred_at,
                        AccountType.USER,
                        Operation.REFUND,
                        EntryStatus.ACCEPTED
                    )
                )
            case StatusDeal.INSPECTION:
                self._entries.append(
                    PostingEntry(
                        self._members.seller_id,
                        agreement.calculate_payment_to_seller(self._price),
                        occurred_at,
                        AccountType.SELLER,
                        Operation.SALE,
                        EntryStatus.FREEZ
                    )
                )
                self._entries.append(
                    PostingEntry(
                        agreement._manager_id,
                        agreement.calculate_sales_profit(self._price),
                        occurred_at,
                        AccountType.MANAGER,
                        Operation.SALE,
                        EntryStatus.ACCEPTED
                    )
                )
        self._status = StatusDeal.ADMIN_CLOSED

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OverdueDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)