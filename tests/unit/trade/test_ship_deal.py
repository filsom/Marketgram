from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.errors import (
    OVERDUE_SHIPMENT, 
    RE_ADD, 
    AddLinkError, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class TestShipDeal:
    def test_adding_download_link_to_the_hand_shipping_deal(self) -> None:
        # Arrange
        deal = self.make_deal(Shipment.HAND)

        # Act
        deal.add_download_link(
            'https://download_link/test', 
            datetime.now(UTC)
        )

        # Assert
        assert deal.download_link is not None

    def test_re_adding_download_link_to_hand_shipping_deal(self) -> None:
        # Arrange
        deal = self.make_deal(Shipment.HAND)
        deal.add_download_link(
            'https://download_link/test',
            datetime.now(UTC)
        )

        # Act
        with pytest.raises(AddLinkError) as excinfo:
            deal.add_download_link(
                'https://download_link/test',
                datetime.now(UTC)
            )
        
        # Assert
        assert str(excinfo.value) == RE_ADD

    def test_adding_dowload_link_after_the_deadline(self) -> None:
        # Arrange
        deal = self.make_deal(
            Shipment.HAND, 
            created_at=datetime.now(UTC) - timedelta(hours=2)
        )

        # Act
        with pytest.raises(CheckDeadlineError) as excinfo:
            deal.add_download_link(
                'https://download_link/test',
                datetime.now(UTC)
            )

        # Assert
        assert str(excinfo.value) == OVERDUE_SHIPMENT

    def make_deal(
        self,
        shipment: Shipment,
        download_link: str | None = None,
        created_at: datetime | None = None
    ) -> ShipDeal:
        if created_at is None:
            created_at = datetime.now(UTC)

        deadlines = ActionTime(1, 1).create_deadlines(created_at)
        return ShipDeal(
            1,
            Members(uuid4(), uuid4()),
            10,
            shipment,
            Money(200),
            deadlines,
            StatusDeal.NOT_SHIPPED,
            created_at,
            1,
            download_link
        )