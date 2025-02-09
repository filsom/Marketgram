from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.errors import (
    AUTO_LINK,
    IN_THE_CHAT,
    MISSING_DOWNLOAD_LINK,
    OVERDUE_SHIPMENT, 
    RE_ADD, 
    AddLinkError, 
    CheckDeadlineError
)
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.trade_item.action_time import ActionTime


class TestShipDeal:
    @pytest.mark.parametrize(
        'shipment, count_notification', [(Shipment.AUTO, 0), (Shipment.HAND, 1), (Shipment.CHAT, 1)]
    )
    def test_sending_notification_to_the_seller_about_the_creation_deal_for_the_purchased_card(
        self, shipment, count_notification
    ) -> None:
        # Arrange
        deal = self.make_deal(shipment)

        # Act
        deal.notify_seller()

        # Assert
        assert len(deal.events) == count_notification

    def test_confirmation_of_shipment_without_download_link_with_delivery_in_chat(self) -> None:
        # Arrange
        occurred_at = datetime.now(UTC)
        deal = self.make_deal(Shipment.CHAT, download_link=None)

        # Act
        deal.confirm_shipment(occurred_at)

        # Assert
        assert len(deal.events) == 0
        assert deal.status == StatusDeal.INSPECTION
        assert deal.shipped_at == occurred_at

    @pytest.mark.parametrize('shipment', [Shipment.HAND, Shipment.AUTO]) 
    def test_confirmation_of_shipping_without_download_link(self, shipment) -> None:
        # Arrange
        deal = self.make_deal(shipment, download_link=None)

        # Act
        with pytest.raises(AddLinkError) as excinfo:
            deal.confirm_shipment(datetime.now(UTC))

        # Assert
        assert str(excinfo.value) == MISSING_DOWNLOAD_LINK
        assert len(deal.events) == 0
        assert deal.status == StatusDeal.NOT_SHIPPED
        assert deal.shipped_at is None

    @pytest.mark.parametrize('shipment', [Shipment.HAND, Shipment.AUTO]) 
    def test_the_seller_has_shipped_the_item_and_confirmed_the_shipment(self, shipment) -> None:
        # Arrange
        occurred_at = datetime.now(UTC)
        deal = self.make_deal(
            shipment,
            download_link='https://download_link/test'
        )

        # Act
        deal.confirm_shipment(occurred_at)

        # Assert
        assert len(deal.events) == 1
        assert deal.status == StatusDeal.INSPECTION
        assert deal.shipped_at == occurred_at

    def test_the_seller_did_not_ship_the_item_on_time(self) -> None:
        # Arrange 
        deal = self.make_deal(
            Shipment.HAND,
            created_at=datetime.now(UTC) - timedelta(hours=2)
        )

        # Act
        with pytest.raises(CheckDeadlineError) as excinfo:
            deal.confirm_shipment(datetime.now(UTC))

        # Assert
        assert str(excinfo.value) == OVERDUE_SHIPMENT
        assert len(deal.events) == 0
        assert deal.shipped_at is None
        assert deal.status == StatusDeal.NOT_SHIPPED

    @pytest.mark.parametrize('shipment', [Shipment.HAND, Shipment.AUTO]) 
    def test_adding_download_link_to_deal(self, shipment) -> None:
        # Arrange
        deal = self.make_deal(shipment)

        # Act
        deal.add_download_link(
            'https://download_link/test', 
            datetime.now(UTC)
        )

        # Assert
        assert deal.download_link is not None

    @pytest.mark.parametrize(
        'shipment, excvalue', [(Shipment.HAND, RE_ADD), (Shipment.AUTO, AUTO_LINK)]
    )
    def test_re_adding_download_link_to_deal(self, shipment, excvalue) -> None:
        # Arrange
        deal = self.make_deal(
            shipment, 
            download_link='https://download_link/test'
        )

        # Act
        with pytest.raises(AddLinkError) as excinfo:
            deal.add_download_link(
                'https://download_link/test',
                datetime.now(UTC)
            )
        
        # Assert
        assert str(excinfo.value) == excvalue

    def test_adding_download_link_for_deal_with_shipment_in_chat(self) -> None:
        # Arrange
        deal = self.make_deal(Shipment.CHAT)

        # Act
        with pytest.raises(AddLinkError) as excinfo:
            deal.add_download_link(
                'https://download_link/test',
                datetime.now(UTC)
            )
        
        # Assert
        assert str(excinfo.value) == IN_THE_CHAT

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