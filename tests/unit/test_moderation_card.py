from datetime import UTC, datetime
from decimal import Decimal

from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.status_card import StatusCard
from marketgram.trade.domain.model.trade_item.items_features.telegram import Description


class TestModerationCard:
    def test_create_new_card(self) -> None:
        # Arrange
        category = self.make_category()

        # Act
        result = category.new_card(
            1,
            Description('Telegram Accounts!', 'TDATA/SESSION+JSON'),
            Money('200'),
            {'spam_block': False},
            {'shipping_hours': 1, 'receipt_hours': 1, 'inspection_hours': 1},
            datetime.now(UTC)
        )

        # Assert
        assert result.status == StatusCard.ON_MODERATION
        assert result.action_time == ActionTime(1, 1, 1)

    def test_create_new_card_with_default_action_time(self) -> None:
        # Arrange
        category = self.make_category()

        # Act
        result = category.new_card(
            1,
            Description('Telegram Accounts!', 'TDATA/SESSION+JSON'),
            Money('200'),
            {'spam_block': False},
            None,
            datetime.now(UTC)
        )

        # Assert
        assert result.status == StatusCard.ON_MODERATION
        assert result.action_time == category.action_time

    def make_category(self) -> Category:
        return Category(
            1,
            1,
            'telegram-123456',
            ActionTime(1, 1, 1),
            TypeDeal.PROVIDING_CODE,
            StatusDeal.NOT_SHIPPED,
            Decimal('0.1'),
            Money(100),
            Decimal('0.1'),
            1
        )