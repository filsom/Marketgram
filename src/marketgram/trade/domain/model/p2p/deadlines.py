from dataclasses import dataclass
from datetime import timedelta

from marketgram.trade.domain.model.trade_item1.exceptions import DomainError


@dataclass(frozen=True)
class Deadlines:
    shipping_hours: int | None
    receipt_hours: int | None
    inspection_hours: int

    def __post_init__(self) -> None:
        for key in self.__dict__:
            if self.__dict__[key] is not None and self.__dict__[key] < 1:
                raise DomainError()

    @property 
    def total_shipping_hours(self) -> timedelta:
        return timedelta(hours=self.shipping_hours)
    
    @property 
    def total_receipt_hours(self) -> timedelta:
        return timedelta(hours=self.receipt_hours)
    
    @property 
    def total_check_hours(self) -> timedelta:
        return timedelta(hours=self.inspection_hours)
    
    def __repr__(self):
        return (
            f'{self.shipping_hours}ч. на отгрузку товара, '
            f'{self.receipt_hours}ч. на подтверждение получения товара, '
            f'{self.inspection_hours}ч. на проверку товара.'
        )