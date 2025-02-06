from datetime import datetime

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.entries import PostingEntry
from marketgram.trade.domain.model.statuses import EntryStatus, StatusDeal
from marketgram.trade.domain.model.types import AccountType, Operation


class OverdueDeal:
    def __init__(
        self, 
        deal_id: int,
        members: Members,
        unit_price: Money,
        status: StatusDeal,
        entries: list[PostingEntry]
    ):
        self._deal_id = deal_id
        self._members = members
        self._unit_price = unit_price
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
                        self._unit_price,
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
                        agreement.calculate_payment_to_seller(self._unit_price),
                        occurred_at,
                        AccountType.SELLER,
                        Operation.SALE,
                        EntryStatus.FREEZ
                    )
                )
                self._entries.append(
                    PostingEntry(
                        agreement._manager_id,
                        agreement.calculate_sales_profit(self._unit_price),
                        occurred_at,
                        AccountType.MANAGER,
                        Operation.SALE,
                        EntryStatus.ACCEPTED
                    )
                )        
        self._status = StatusDeal.ADMIN_CLOSED

    @property
    def status(self) -> StatusDeal:
        return self._status

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OverdueDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)