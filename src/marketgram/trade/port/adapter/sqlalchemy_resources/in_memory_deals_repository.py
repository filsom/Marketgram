from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from marketgram.trade.domain.model.p2p.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.receipt_deal import ReceiptDeal
from marketgram.trade.domain.model.p2p.ship_deal import (
    ShipDeal, 
    ShipLoginCodeDeal, 
    ShipProvidingLinkDeal
)
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.rule.agreement.deal_rule import (
    PaymentFormula, 
    PaymentTaxFormula
)
from marketgram.trade.domain.model.rule.agreement.entry import PostingEntry
from marketgram.trade.domain.model.rule.agreement.entry_status import EntryStatus
from marketgram.trade.domain.model.rule.agreement.limits import Limits
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.rule.agreement.service_agreement import (
    ServiceAgreement
)
from marketgram.trade.domain.model.rule.agreement.types import (
    AccountType, 
    EventType, 
    Operation
)


class InMemoryDealsRepository:
    def __init__(self):
        self.deals: dict[UUID, ShipDeal] = {}
        self._entries: list[PostingEntry] = []

    def add(self, deal: ShipDeal) -> None:
        self.deals[deal._deal_id] = deal

    async def unshipped_with_id(
        self, 
        seller_id: UUID,
        deal_id: UUID
    ) -> ShipDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if (deal._seller_id != seller_id 
            or deal._status != StatusDeal.NOT_SHIPPED):
            return None
        
        if deal._type_deal == TypeDeal.AUTO_LINK:
            return deal
        
        elif deal._type_deal == TypeDeal.PROVIDING_CODE:
            return ShipLoginCodeDeal(
                deal._deal_id,
                deal._seller_id,
                deal._buyer_id,
                deal._card_id,
                deal._qty_purchased,
                deal._type_deal,
                deal._card_created_at,
                deal._price,
                deal._time_tags,
                deal._deadlines,
                deal._status
            )
        
        elif deal._type_deal == TypeDeal.PROVIDING_LINK:
            return ShipProvidingLinkDeal(
                deal._deal_id,
                deal._seller_id,
                deal._buyer_id,
                deal._card_id,
                deal._qty_purchased,
                deal._type_deal,
                deal._card_created_at,
                deal._price,
                deal._time_tags,
                deal._deadlines,
                deal._status
            )
    
    async def unreceived_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> ReceiptDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if (deal._buyer_id != buyer_id
            or deal._status != StatusDeal.AWAITING):
            return None
        
        return ReceiptDeal(
            deal._deal_id,
            deal._time_tags,
            deal._deadlines,
            deal._status
        )

    async def unconfirmed_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> ConfirmationDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if (deal._buyer_id != buyer_id
            or deal._status != StatusDeal.CHECK):
            return None
        
        agr = ServiceAgreement(uuid4())
        agr.new_limits(
            Limits(
                Money(100), 
                Money(100), 
                Money(100), 
                Decimal(0.1), 
                Decimal(0.1), 
                Decimal(0.1), 
                datetime.now()
            )
        )
        agr.add_rule(
            EventType.PRODUCT_CONFIRMED, 
            PaymentFormula(
                AccountType.SELLER, 
                Operation.PAYMENT, 
                EntryStatus.FREEZ
            )
        )
        agr.add_rule(
            EventType.TAX_PAYMENT, 
            PaymentTaxFormula(
                UUID('683b21bc-bc2d-4776-81c8-900593c7b698'), 
                AccountType.TAX, 
                Operation.PAYMENT, 
                EntryStatus.FREEZ)
        )
        confirmation_deal = ConfirmationDeal(
            deal._deal_id,
            deal._card_created_at,
            deal._time_tags,
            deal._deadlines,
            deal._status,
            self._entries
        )
        confirmation_deal.accept_agreement(agr)

        return confirmation_deal

    async def unclosed_with_id(
        self,
        seller_id: UUID,
        deal_id: UUID
    ) -> CancellationDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if deal._seller_id != seller_id or deal._status in [
            StatusDeal.CANCELLED, 
            StatusDeal.CLOSED
        ]:
            return None
        
        return CancellationDeal(
            deal._deal_id,
            deal._buyer_id,
            deal._price,
            deal._time_tags,
            deal._status,
            self._entries
        )
    
    async def not_disputed_with_id(
        self,
        buyer_id: UUID,
        deal_id: UUID
    ) -> DisputeDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if deal._buyer_id != buyer_id or deal._status in [
            StatusDeal.DISPUTE,
            StatusDeal.CLOSED,
            StatusDeal.CANCELLED
        ]:
            return None
        
        return DisputeDeal(
            deal._deal_id,
            deal._buyer_id,
            deal._seller_id,
            deal._price,
            deal._is_disputed,
            deal._time_tags,
            deal._deadlines,
            self._entries,
            deal._status,
            None
        )
    
    async def disputed_with_id(
        self,
        deal_id: UUID,
    ) -> DisputeDeal | None:
        deal: ShipDeal = self.deals.get(deal_id, None)
        if deal is None:
            return None
        
        if deal._status != StatusDeal.DISPUTE:
            return None
        
        return DisputeDeal(
            deal._deal_id,
            deal._buyer_id,
            deal._seller_id,
            deal._price,
            deal._is_disputed,
            deal._time_tags,
            deal._deadlines,
            self._entries,
            deal._status,
            None
        )