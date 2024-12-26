from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from enum import StrEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marketgram.trade.domain.model.p2p.user import QuantityPurchased


class Currency(StrEnum):
    RUB = auto()

    def mark(self) -> str:
        return '₽'


@dataclass(frozen=True, order=True)
class Money:
    number: str | int | Decimal
    currency: Currency = field(default=Currency.RUB)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, 
            'number', 
            Decimal(str(self.number))
            .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
        )

    def round_up(self) -> Money:
        value = self.number.quantize(Decimal('1'), ROUND_HALF_UP)
        return Money(value)

    def __repr__(self) -> str:
        return f'{self.number}{self.currency.mark()}'

    def __abs__(self) -> Money:
        return Money(abs(self.number))

    def __mul__(self, value: int | float | Decimal) -> Money:
        if not isinstance(value, (int, float, Decimal)):
            raise TypeError

        if value == 0:
            raise ArithmeticError

        return Money(
            self.number 
            * Decimal(str(value))
            .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
        )

    def __sub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.number - value.number)
    
    def __isub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.number - value.number)

    def __iadd__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.number + value.number)

    def __add__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.number + value.number)

    def __neg__(self) -> Money:
        return Money(-self.number)
    
    def _isinstance(self, value: Money) -> None:
        if not isinstance(value, Money):
            raise TypeError
        
        if self.currency != value.currency:
            raise TypeError