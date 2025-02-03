from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.types import INFINITY


class ServiceAgreement:
    def __init__(
        self,
        manager_id: int,
        payout_tax: Decimal,
        sales_tax: Decimal,
        minimum_payout: Money,
        minimum_payment: Money,
        created_at: datetime,
        archived_in: datetime | str = INFINITY,
        agreement_id: int | None = None
    ) -> None:
        self._agreement_id = agreement_id
        self._manager_id = manager_id
        self._payout_tax = payout_tax
        self._sales_tax = sales_tax
        self._minimum_payout = minimum_payout
        self._minimum_payment = minimum_payment
        self._created_at = created_at
        self._archived_in = archived_in
    
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
    
    def archive(self, current_time: datetime) -> None:
        self._archived_in = current_time
    
    @property
    def manager_id(self) -> UUID:
        return self._manager_id

    @property
    def archived_in(self) -> datetime:
        if self._archived_in == INFINITY:
            return datetime.max
        else:
            return self._archived_in
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ServiceAgreement):
            raise TypeError
        
        return self.archived_in < other.archived_in
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ServiceAgreement):
            return False

        return self._agreement_id == other._agreement_id
    
    def __hash__(self) -> int:
        return hash(self._agreement_id)