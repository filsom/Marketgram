from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.entry import PostingEntry
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.paycard import Paycard


class ServiceAgreement:
    def __init__(
        self,
        manager_id: UUID,
        payout_tax: Decimal,
        sales_tax: Decimal,
        minimum_payout: Money,
        minimum_payment: Money,
        created_at: datetime
    ) -> None:
        self._manager_id = manager_id
        self._payout_tax = payout_tax
        self._sales_tax = sales_tax
        self._minimum_payout = minimum_payout
        self._minimum_payment = minimum_payment
        self._created_at = created_at
    
    def calculate_payment_to_seller(self, price: Money) -> Money:
        return price - price * self._sales_tax
    
    def calculate_sales_profit(self, price: Money) -> Money:
        return price * self._sales_tax

    def calculate_amount_payout(self, tax_free: Money) -> Money:
        return -tax_free + tax_free * self._payout_tax
    
    def calculate_payout_profit(self, tax_free: Money) -> Money:
        return tax_free * self._payout_tax
    
    def check_amount_payout(self, amount_payout: Money) -> bool:
        return amount_payout >= self._minimum_payout

    def check_amount_payment(self, amount_payment: Money) -> bool:
        return amount_payment >= self._minimum_payment
    

class SalesManager:
    def __init__(
        self, 
        user_id: UUID,
        balance: Money,
        entries: list[PostingEntry],
        paycard: Paycard = None
    ) -> None:
        self._user_id = user_id
        self._balance = balance
        self._entries = entries
        self._paycard = paycard

    def new_service_agreement(
        self,
        payout_tax: Decimal,
        sales_tax: Decimal,
        minimum_payout: Money,
        minimum_payment: Money,
        created_at: datetime
    ) -> ServiceAgreement:
        if payout_tax <= Decimal('0'):
            raise DomainError()

        if sales_tax <= Decimal('0'):
            raise DomainError()
        
        if minimum_payout <= Money('0'):
            raise DomainError()
        
        if minimum_payment <= Money('0'):
            raise DomainError()
        
        return ServiceAgreement(
            self._user_id,
            payout_tax,
            sales_tax,
            minimum_payout,
            minimum_payment,
            created_at
        )
    
    def change_paycard(self, paycard: Paycard) -> None: 
        self._paycard = paycard