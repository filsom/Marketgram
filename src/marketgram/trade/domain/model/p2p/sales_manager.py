from datetime import datetime
from decimal import Decimal
from uuid import UUID

from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.paycard import Paycard
    

class SalesManager:
    def __init__(
        self, 
        user_id: UUID,
        balance: Money,
        entries: list[PostingEntry],
        service_agreements: list[ServiceAgreement],
        paycard: Paycard | None = None
    ) -> None:
        self._user_id = user_id
        self._balance = balance
        self._entries = entries
        self._paycard = paycard
        self._service_agreements = service_agreements

    def new_service_agreement(
        self,
        payout_tax: Decimal,
        sales_tax: Decimal,
        minimum_payout: Money,
        minimum_payment: Money,
        current_time: datetime
    ) -> None:
        if payout_tax <= Decimal('0'):
            raise DomainError()

        if sales_tax <= Decimal('0'):
            raise DomainError()
        
        if minimum_payout <= Money('0'):
            raise DomainError()
        
        if minimum_payment <= Money('0'):
            raise DomainError()
        
        if self._service_agreements:
            last_agreement = sorted(self._service_agreements)[-1]
            last_agreement.archive(current_time)

        self._service_agreements.append(
            ServiceAgreement(
                self._user_id,
                payout_tax,
                sales_tax,
                minimum_payout,
                minimum_payment,
                current_time,
            )
        )
    
    def change_paycard(self, paycard: Paycard) -> None: 
        self._paycard = paycard

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SalesManager):
            return False

        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)