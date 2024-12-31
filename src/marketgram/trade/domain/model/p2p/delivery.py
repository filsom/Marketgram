from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from marketgram.trade.domain.model.trade_item.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.spa.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.p2p.transfer_method import TransferMethod
from marketgram.trade.domain.model.p2p.format import Format
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal


@dataclass(frozen=True)
class Delivery:
    format: Format
    method: TransferMethod

    def __post_init__(self) -> None:
        if self.method.is_auto() and self.format.is_code():
            raise DomainError()
        
    def what_type(self) -> TypeDeal:
        if self.is_auto_link():
            return TypeDeal.AUTO_LINK

        if self.is_providing_link():
            return TypeDeal.PROVIDING_LINK
        
        if self.is_providing_code():
            return TypeDeal.PROVIDING_CODE

    def what_stage(self) -> StatusDeal:
        if self.is_auto_link():
            return StatusDeal.CHECK

        if self.is_providing_link():
            return StatusDeal.NOT_SHIPPED
        
        if self.is_providing_code():
            return StatusDeal.NOT_SHIPPED    

    def calculate_deadlines(
        self,
        shipping_hours: int | None,
        receipt_hours: int | None,
        check_hours: int
    ) -> Deadlines | None:
        if self.is_auto_link():
            return Deadlines(
                None, 
                None, 
                check_hours
            )
        if self.is_providing_link():
            if None in (shipping_hours, receipt_hours):
                raise DomainError()
            
            return Deadlines(
                shipping_hours, 
                receipt_hours, 
                check_hours
            )
        if self.is_providing_code():
            return None

    def from_stock(self) -> bool:
        if self.method.is_auto() and self.format.is_link():
            return True
        
        return False
    
    def provide_time_tags(self, bought_in: datetime) -> TimeTags:
        time_tags = TimeTags(bought_in)

        if self.is_auto_link():
            time_tags = time_tags.shipped(bought_in).received(bought_in)

        return time_tags
    
    def is_auto_link(self) -> bool:
        return self.method.is_auto() and self.format.is_link()
    
    def is_providing_link(self) -> bool:
        return self.method.is_provides_seller() and self.format.is_link()
    
    def is_providing_code(self) -> bool:
        return self.method.is_provides_seller() and self.format.is_code()