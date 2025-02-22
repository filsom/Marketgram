from __future__ import annotations

from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from enum import StrEnum, auto
from functools import total_ordering


class Currency(StrEnum):
    RUB = auto()

    def mark(self) -> str:
        return '₽'
        

@total_ordering
class Money:
    def __init__(self, value: str | int) -> None:
        self._value = Decimal(str(value)) \
            .quantize(Decimal('1.00'), ROUND_HALF_EVEN)
        self._currency = Currency.RUB

    def round_up(self) -> Money:
        value = self._value.quantize(Decimal('1'), ROUND_HALF_UP)
        return Money(value)

    def __repr__(self) -> str:
        return f'{self._value}{self._currency.mark()}'

    def __abs__(self) -> Money:
        return Money(abs(self._value))

    def __mul__(self, value: Decimal | int) -> Money:
        if not isinstance(value, (int, Decimal)):
            raise TypeError

        if value == 0:
            raise ArithmeticError

        return Money(self._value * value)

    def __sub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self._value - value._value)
    
    def __isub__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self._value - value._value)

    def __iadd__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self._value + value._value)

    def __add__(self, value: Money) -> Money:
        self._isinstance(value)
        return Money(self._value + value._value)

    def __neg__(self) -> Money:
        return Money(-self._value)
    
    def __lt__(self, value: Money) -> bool:
        self._isinstance(value)

        return self._value < value._value
    
    def __eq__(self, value: Money) -> bool:
        self._isinstance(value)

        return self._value == value._value
    
    def _isinstance(self, value: Money) -> None:
        if not isinstance(value, Money):
            raise TypeError
        
        if self._currency != value._currency:
            raise TypeError