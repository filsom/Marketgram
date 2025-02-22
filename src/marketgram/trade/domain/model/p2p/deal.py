from datetime import datetime, timedelta

from marketgram.common.entity import Entity
from marketgram.trade.domain.model.entries import PostingEntry
from marketgram.trade.domain.model.events import (
    DisputeClosedEvent, 
    SellerShippedItemManuallyEvent
)
from marketgram.trade.domain.model.notifications import (
    DealCreatedNotification,
    DisputeOpenedNotification,
    SellerCancelledDealNotification,
    ShippedByDealNotification,
)
from marketgram.trade.domain.model.p2p.claim import Claim, ReturnType
from marketgram.trade.domain.model.p2p.dispute import OpenedDispute
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.errors import (
    DO_NOT_OPEN_DISPUTE,
    LATE_CONFIRMATION,
    MISSING_DOWNLOAD_LINK,
    OVERDUE_SHIPMENT,
    PAYMENT_TO_SELLER,
    RETURN_TO_BUYER,
    AddLinkError, 
    CheckDeadlineError,
    QuantityItemError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.statuses import EntryStatus, StatusDeal, StatusDispute
from marketgram.trade.domain.model.types import AccountType, Operation


class Deal(Entity):
    def __init__(
        self, 
        deal_id: int | None,
        status: StatusDeal, 
        unit_price: Money,
        qty_purchased: int
    ) -> None:
        super().__init__()
        self._deal_id = deal_id
        self._status = status
        self._unit_price = unit_price
        self._qty_purchased = qty_purchased

    @property
    def status(self) -> StatusDeal:
        return self._status
    
    @property
    def deal_id(self) -> int | None:
        return self._deal_id
    
    @property
    def amount_deal(self) -> Money:
        return self._unit_price * self._qty_purchased
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Deal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)
    

class ShipDeal(Deal):
    def __init__(
        self,
        card_id: int,
        members: Members,
        qty_purchased: int,
        shipment: Shipment,
        unit_price: Money,
        deadlines: Deadlines,
        status: StatusDeal,
        created_at: datetime,
        shipped_at: datetime = None
    ) -> None:
        super().__init__(
            None,
            status,
            unit_price,
            qty_purchased
        )
        self._card_id = card_id
        self._members = members
        self._shipment = shipment
        self._deadlines = deadlines
        self._created_at = created_at
        self._shipped_at = shipped_at

    def confirm_shipment(
        self, 
        occurred_at: datetime,
        download_link: str | None = None
    ) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            raise CheckDeadlineError(OVERDUE_SHIPMENT)
            
        if self._shipment.is_not_auto_link():
            if self._shipment.is_hand():
                if download_link is None:
                    raise AddLinkError(MISSING_DOWNLOAD_LINK)   

                self.add_event(
                    SellerShippedItemManuallyEvent(
                        self._deal_id,
                        download_link,
                        occurred_at
                    )
                ) 
            self.add_event(
                ShippedByDealNotification(
                    self._members.buyer_id,
                    self._deal_id,
                    occurred_at
                )
            )
        self._shipped_at = occurred_at
        self._status = StatusDeal.INSPECTION

    def notify_seller(self) -> None:
        if self._shipment.is_notify_to_the_seller():
            self.add_event(
                DealCreatedNotification(
                    self._members.seller_id,
                    self._deal_id,
                    self._card_id,
                    self._qty_purchased,
                    self._shipped_at,
                    self._created_at
                )
            )

    @property
    def write_off_ammount(self) -> Money:
        return -self._unit_price * self._qty_purchased
    
    @property
    def shipped_at(self) -> datetime | None:
        return self._shipped_at
    
    @property 
    def qty_purchased(self) -> int:
        return self._qty_purchased
    

class UnconfirmedDeal(Deal):
    def __init__(
        self, 
        deal_id: int,
        card_id: int,
        members: Members,
        unit_price: Money,
        qty_purchased: int,
        deadlines: Deadlines,
        shipment: Shipment,
        status: StatusDeal,
        inspected_at: datetime | None,
        entries: list[PostingEntry]
    ) -> None:
        super().__init__(
            deal_id,
            status,
            unit_price,
            qty_purchased
        )
        self._card_id = card_id
        self._members = members
        self._deadlines = deadlines
        self._shipment = shipment
        self._inspected_at = inspected_at
        self._entries = entries

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
    ) -> OpenedDispute:   
        if not self._deadlines.check(self._status, occurred_at):
            raise CheckDeadlineError(DO_NOT_OPEN_DISPUTE)
        
        if qty_defects > self._qty_purchased:
            raise QuantityItemError()

        self._status = StatusDeal.DISPUTE
        self.add_event(
            DisputeOpenedNotification(
                self._members.seller_id, 
                occurred_at
            )
        )        
        return OpenedDispute(
            self._card_id,
            Claim(qty_defects, reason, return_type),
            self._members.start_dispute(self._deal_id),
            self._shipment,
            occurred_at,
            occurred_at + timedelta(days=1),
            StatusDispute.OPEN
        )
    
    @property
    def inspected_at(self) -> datetime:
        return self._inspected_at
    
    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries
    
    @property
    def amount_deal(self) -> Money:
        return self._unit_price * self._qty_purchased
    

class FailDeal(Deal):
    def __init__(
        self,
        deal_id: int,
        buyer_id: int,
        unit_price: Money,
        qty_purchased: int,
        deadlines: Deadlines,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        super().__init__(
            deal_id,
            status,
            unit_price,
            qty_purchased
        )
        self._buyer_id = buyer_id
        self._deadlines = deadlines
        self._entries = entries

    def cancel(self, occurred_at: datetime) -> None:
        if not self._deadlines.check(self._status, occurred_at):
            match self._status:
                case StatusDeal.NOT_SHIPPED:
                    raise CheckDeadlineError(RETURN_TO_BUYER)
                
                case StatusDeal.INSPECTION:
                    raise CheckDeadlineError(PAYMENT_TO_SELLER)     

        self._entries.append(
            PostingEntry(
                self._buyer_id,
                self.amount_deal,
                occurred_at,
                AccountType.USER,
                Operation.REFUND,
                EntryStatus.ACCEPTED
            )
        )
        self.add_event(
            SellerCancelledDealNotification(
                self._buyer_id,
                self._deal_id,
                occurred_at
            )
        )
        self._status = StatusDeal.CANCELLED
    
    @property
    def entries(self) -> list[PostingEntry]:
        return self._entries
    

class DisputeDeal(Deal):
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
        super().__init__(
            deal_id,
            status,
            unit_price,
            qty_purchased
        )
        self._members = members
        self._deadlines = deadlines
        self._entries = entries

    def allocate_money(
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

        self.add_event(
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
        self.add_event(
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
        self.add_event(
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
    def entries(self) -> list[PostingEntry]:
        return self._entries
    

class OverdueDeal(Deal):
    def __init__(
        self, 
        deal_id: int,
        members: Members,
        unit_price: Money,
        qty_purchased: int,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        super().__init__(
            deal_id,
            status,
            unit_price,
            qty_purchased
        )
        self._members = members
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
                        self.amount_deal,
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