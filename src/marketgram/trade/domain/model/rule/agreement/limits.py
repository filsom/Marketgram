from dataclasses import dataclass
from datetime import datetime
from typing import get_type_hints
from decimal import ROUND_HALF_EVEN, Decimal

from marketgram.trade.domain.model.trade_item.exceptions import (
    INCORRECT_VALUES, 
    DomainError
)
from marketgram.trade.domain.model.rule.agreement.money import (
    Money
)


@dataclass(frozen=True)
class Limits:
    min_price: Money
    min_withdraw: Money
    min_deposit: Money
    min_discount: Decimal
    tax_payment: Decimal
    tax_payout: Decimal
    install_date: datetime

    def __post_init__(self) -> None:
        for name, type in get_type_hints(self).items():
            value = getattr(self, name)
            if issubclass(type, Money) and value <= Money(0):
                raise DomainError(INCORRECT_VALUES.format(name))
            
            if issubclass(type, Decimal) and (value <= 0 or value >= 1):
                raise DomainError(INCORRECT_VALUES.format(name))

            if issubclass(type, Decimal):
                object.__setattr__(
                    self, 
                    name, 
                    Decimal(value) \
                    .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
                )