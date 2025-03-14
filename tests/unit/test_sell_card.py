from datetime import UTC, datetime

import pytest

from marketgram.trade.domain.model.entries import PriceEntry
from marketgram.trade.domain.model.errors import (
    QuantityItemError,
    ReplacingItemError, 
    CurrentСardStateError
)
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.sell_card import SellCard, SellStockCard


class TestSellCard:
    @pytest.mark.parametrize('shipment', [Shipment.HAND, Shipment.CHAT])
    def test_purchase_card(self, shipment):
        # Arrange
        card = self.make_sell_card([PriceEntry(1, Money(200))], shipment)

        # Act
        card.purchase(2, Money(200), shipment, 10, datetime.now(UTC))

        # Assert
        assert len(card.release_events()) == 1
        assert card.status == StatusCard.PURCHASED

    def test_purchase_stock_card(self):
        # Arrange
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], 200, Shipment.AUTO)

        # Act
        stock_card.purchase(2, Money(200), Shipment.AUTO, 100, datetime.now(UTC))

        # Assert
        assert len(stock_card.inventory_entries) == 1
        assert len(stock_card.release_events()) == 1
        assert stock_card.status == StatusCard.ON_SALE

    @pytest.mark.parametrize('qty', [0, -1, 1000])
    def test_purchase_with_incorrect_quantity(self, qty):
        # Arrange
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], stock_balance=200)

        # Act
        with pytest.raises(QuantityItemError):
            stock_card.purchase(2, Money(200), Shipment.AUTO, qty, datetime.now(UTC))

        # Assert
        assert len(stock_card.inventory_entries) == 0
        assert len(stock_card.release_events()) == 0
        assert stock_card.status == StatusCard.ON_SALE

    def test_replacement_of_purchased_item_in_regular_card(self):
        # Arrange
        card = self.make_sell_card([PriceEntry(1, Money(200))], Shipment.HAND)

        # Act
        with pytest.raises(ReplacingItemError):
            card.replace(20, datetime.now(UTC))

    def test_replacement_of_purchased_item_in_stock_card(self):
        # Arrange
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], 200)

        # Act
        stock_card.replace(100, datetime.now(UTC))

        # Assert
        assert len(stock_card.inventory_entries) == 1
        assert stock_card.status == StatusCard.ON_SALE
        assert stock_card.shipment == Shipment.AUTO

    @pytest.mark.parametrize('qty', [0, -1, 1000])
    def test_replacement_of_incorrect_quantity(self, qty):
        # Arrange
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], stock_balance=200)

        # Act
        with pytest.raises(ReplacingItemError):
            stock_card.replace(qty, datetime.now(UTC))

    def test_editing_sales_card(self):
        # Arrange
        card = self.make_sell_card([PriceEntry(1, Money(200))], Shipment.HAND)

        # Act
        card.edit()

        # Assert
        assert card.status == StatusCard.EDITING        

    def test_purchase_ended_with_zero_balance_on_the_card(self):
        # Arrange
        qty = 200
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], stock_balance=qty)

        # Act
        stock_card.purchase(2, Money(200), Shipment.AUTO, qty, datetime.now(UTC))

        # Assert
        assert len(stock_card.inventory_entries) == 1
        assert len(stock_card.release_events()) == 2
        assert stock_card.status == StatusCard.PURCHASED
        assert stock_card.shipment == Shipment.HAND

    @pytest.mark.parametrize('status', [StatusCard.EDITING, StatusCard.PURCHASED])
    def test_purchase_of_a_non_sale_card(self, status):
        # Arrange
        card = self.make_sell_card([PriceEntry(1, Money(200))], Shipment.HAND, status_card=status)

        # Act
        with pytest.raises(CurrentСardStateError):
            card.purchase(2, Money(200), Shipment.HAND, 10, datetime.now(UTC))
    
    def test_purchase_with_changed_conditions(self):
        # Arrange
        card = self.make_sell_card([PriceEntry(1, Money(200))], Shipment.HAND)

        # Act
        with pytest.raises(CurrentСardStateError):
            card.purchase(2, Money(250), Shipment.HAND, 10, datetime.now(UTC))

    def test_purchase_from_stock_with_changed_shipping_conditions(self):
        # Arrange
        stock_card = self.make_sell_stock_card([PriceEntry(1, Money(200))], 200, Shipment.HAND)

        # Act
        with pytest.raises(CurrentСardStateError):
            stock_card.purchase(2, Money(200), Shipment.AUTO, 100, datetime.now(UTC))

    def make_sell_card(
        self, 
        unit_price: list[PriceEntry],
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
        unit_price: list[PriceEntry],
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