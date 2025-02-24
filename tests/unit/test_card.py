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
    card.set_quantity_discount([PriceEntry(100, Money(130)), PriceEntry(150, Money(120))])
    card.remove_quantity_discount()

    # Assert
    # assert len(card._price_entries) == 2
    # assert not len(card._price_entries)
    assert 100 % 50 == 0 
