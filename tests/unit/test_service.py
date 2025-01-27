from decimal import Decimal

from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item.category import CategoryType, Service


class TestService:
    def test_create_new_service_category(self) -> None:
        # Arrange
        service = Service('telegram', 'telegram-123456', service_id=1, categories_id=[])
        category_type = CategoryType('Accounts', 1)
        # Act
        result = service.create_new_category(
            'Accounts TDATA_SJ',
            category_type.category_type_id,
            Money(100), 
            Decimal('0.1'), 
        )

        # Assert
        assert result._category_name == 'Accounts TDATA_SJ'.lower()
        assert result._minimum_discount_rate == Decimal('0.1')
        assert result._minimum_price == Money('100')
        