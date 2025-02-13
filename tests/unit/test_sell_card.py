from datetime import UTC, datetime

import pytest

from marketgram.trade.domain.model.errors import CurrentСardStateError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.trade_item.sell_stock_card import SellStockCard


class TestSellCard:
    @pytest.mark.parametrize('shipment', [Shipment.HAND, Shipment.CHAT])
    def test_purchase_card(self, shipment):
        # Arrange
        card = self.make_sell_card(Money(200), shipment)

        # Act
        card.purchase(2, Money(200), shipment, 10, datetime.now(UTC))

        # Assert
        assert len(card.release()) == 1
        assert card.status == StatusCard.PURCHASED

    @pytest.mark.parametrize('status', [StatusCard.EDITING, StatusCard.PURCHASED])
    def test_purchase_of_a_non_sale_card(self, status):
        # Arrange
        card = self.make_sell_card(Money(200), Shipment.HAND, status_card=status)

        # Act
        with pytest.raises(CurrentСardStateError):
            card.purchase(2, Money(200), Shipment.HAND, 10, datetime.now(UTC))
    
    def test_purchase_with_changed_conditions(self):
        # Arrange
        card = self.make_sell_card(Money(200), Shipment.HAND)

        # Act
        with pytest.raises(CurrentСardStateError):
            card.purchase(2, Money(250), Shipment.HAND, 10, datetime.now(UTC))

    def test_purchase_from_stock_with_changed_shipping_conditions(self):
        # Arrange
        stock_card = self.make_sell_stock_card(Money(200), 200, Shipment.HAND)

        # Act
        with pytest.raises(CurrentСardStateError):
            stock_card.purchase(2, Money(200), Shipment.AUTO, 100, datetime.now(UTC))

    def make_sell_card(
        self, 
        unit_price: Money,
        shipment: Shipment,
        status_card: StatusCard = StatusCard.ON_SALE
    ) -> SellCard:
        return SellCard(
            1,
            1,
            unit_price,
            shipment,
            ActionTime(1, 1),
            status_card
        )
    
    def make_sell_stock_card(
        self, 
        unit_price: Money,
        stock_balance: int,
        shipment: Shipment = Shipment.AUTO,
        status_card: StatusCard = StatusCard.ON_SALE
    ) -> SellStockCard:
        return SellStockCard(
            1,
            1,
            unit_price,
            shipment,
            ActionTime(1, 1),
            status_card,
            stock_balance,
            []
        )