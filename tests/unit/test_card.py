from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from marketgram.trade.domain.model.card import Card
from marketgram.trade.domain.model.description import (
    AccountFormat, 
    Description, 
    Region
)
from marketgram.trade.domain.model.exceptions import (
    DISCOUNT_ERROR, 
    DomainError
)
from marketgram.trade.domain.model.p2p.delivery import Delivery
from marketgram.trade.domain.model.p2p.format import Format
from marketgram.trade.domain.model.p2p.transfer_method import (
    TransferMethod
)
from marketgram.trade.domain.model.rule.agreement.money import Money


class TestCard:
    def test_new_discounted_price(self) -> None:
        # Arrange
        new_price = Money(150)
        sut = self.make_card(Money(200), Money(100), Decimal('0.1'))

        # Act
        sut.set_discounted_price(new_price)

        # Assert
        assert sut.price == Money(150)

    def test_remove_discount_price(self):
        # Arrange 
        sut = self.make_card(Money(200), Money(100), Decimal('0.1'))
        sut.set_discounted_price(Money(150))

        # Act
        sut.remove_discount()

        # Assert
        assert sut.price == Money(200)

    def test_setting_a_new_price_at_a_minimum_discounted_price(self) -> None:
        # Arrange
        new_price = Money(103)
        min_price = Money(100)

        sut = self.make_card(Money(105), min_price, Decimal('0.1'))

        # Act
        with pytest.raises(DomainError) as excinfo:
            sut.set_discounted_price(new_price)

        # Assert
        assert DISCOUNT_ERROR == str(excinfo.value)

    @pytest.mark.parametrize('incorrect_price', [(Money(10)), (Money(200))])
    def test_incorrect_min_and_max_values_of_the_discounted_price(self, incorrect_price) -> None:
        # Arrange
        min_price = Money(100)

        sut = self.make_card(Money(200), min_price, Decimal('0.1'))

        # Act
        with pytest.raises(DomainError) as excinfo:
            sut.set_discounted_price(incorrect_price)

        # Assert
        assert 'Некорректная скидочная цена!' in str(excinfo.value)
            
    def make_card(
        self, 
        price: Money, 
        min_price: Money, 
        min_discount: Decimal,
    ) -> Card:
        delivery = Delivery(
            Format.LOGIN_CODE,
            TransferMethod.PROVIDES_SELLER
        )
        return Card(
            uuid4(),
            uuid4(),
            price,
            Description(
                'TestCard',
                'Test',
                AccountFormat.Autoreg,
                Region.Other,
                False
            ),
            delivery,
            delivery.calculate_deadlines(1, 1, 1),
            min_price,
            min_discount,
            datetime.now(tz=UTC)
        )