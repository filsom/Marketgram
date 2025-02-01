from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from enum import StrEnum, auto


class Currency(StrEnum):
    RUB = auto()

    def mark(self) -> str:
        return '₽'


@dataclass(frozen=True, order=True)
class Money:
    number: InitVar[str | int]

    value: Decimal | None = None
    currency: Currency = field(default=Currency.RUB)

    def __post_init__(self, number: str | int) -> None:
        object.__setattr__(
            self, 
            'value', 
            Decimal(str(number))
            .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
        )

    def round_up(self) -> Money:
        value = self.value.quantize(Decimal('1'), ROUND_HALF_UP)
        return Money(value)

    def __repr__(self) -> str:
        return f'{self.value}{self.currency.mark()}'

    def __abs__(self) -> Money:
        return Money(abs(self.value))

    def __mul__(self, value: Decimal) -> Money:
        if not isinstance(value, (int, Decimal)):
            raise TypeError

        if value == 0:
            raise ArithmeticError

        return Money(
            self.value 
            * value
            .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
        )

    def __sub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.value - value.value)
    
    def __isub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.value - value.value)

    def __iadd__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.value + value.value)

    def __add__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self.value + value.value)

    def __neg__(self) -> Money:
        return Money(-self.value)
    
    def _isinstance(self, value: Money) -> None:
        if not isinstance(value, Money):
            raise TypeError
        
        if self.currency != value.currency:
            raise TypeError