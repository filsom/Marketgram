from decimal import Decimal
from marketgram.trade.domain.model.entries import PriceEntry
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.card import EditorialCard


def test_set_quantity_discount_price() -> None:
    # Arrange
    card = EditorialCard(
        1, 
        ActionTime(1, 1),
        Shipment.HAND,
        Money(50),
        Decimal('10'),
        StatusCard.EDITING,
        [PriceEntry(1, Money(150))]
    )

    # Act
    card.set_quantity_discount(PriceEntry(3, Money(102)))
    card.set_quantity_discount(PriceEntry(2, Money(146)))
    # card.set_quantity_discount(PriceEntry(10, Money(80)))
    # card.set_quantity_discount(PriceEntry(10, Money(70)))

    # Assert
    assert len(card._price_entries) == 3
    assert not len(card._price_entries)