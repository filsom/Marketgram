from decimal import Decimal
from marketgram.trade.domain.model.entries import PriceEntry
from marketgram.trade.domain.model.money import Money


def test_discount():
    price_entry = PriceEntry(1, Money(200), [])

    discount = price_entry.calculate_discount(Money(180), Money(100), Decimal("10"))

    assert discount == 25

