import pytest

from marketgram.trade.domain.model.p2p.deal.shipment import Shipment


class TestShipment:
    @pytest.mark.parametrize(
        'shipment, value', [
            (Shipment.AUTO, True), 
            (Shipment.HAND, True), 
            (Shipment.CHAT, False)
        ]
    )
    def test_is_link(self, shipment: Shipment, value) -> None:
        # Act
        result = shipment.is_link()

        # Assert
        assert result == value

    @pytest.mark.parametrize(
        'shipment, value', [
            (Shipment.AUTO, False), 
            (Shipment.HAND, True), 
            (Shipment.CHAT, False)
        ]
    )
    def test_is_hand(self, shipment: Shipment, value) -> None:
        # Act
        result = shipment.is_hand()

        # Assert
        assert result == value

    @pytest.mark.parametrize(
        'shipment, value', [
            (Shipment.AUTO, True), 
            (Shipment.HAND, False), 
            (Shipment.CHAT, False)
        ]
    )
    def test_is_auto_link(self, shipment: Shipment, value) -> None:
        # Act
        result = shipment.is_auto_link()

        # Assert
        assert result == value

    @pytest.mark.parametrize(
        'shipment, value', [
            (Shipment.AUTO, True), 
            (Shipment.HAND, False), 
            (Shipment.CHAT, False)
        ]
    )
    def test_is_message(self, shipment: Shipment, value) -> None:
        # Act
        result = shipment.is_auto_link()

        # Assert
        assert result == value

    @pytest.mark.parametrize(
        'shipment, value', [
            (Shipment.AUTO, False), 
            (Shipment.HAND, True), 
            (Shipment.CHAT, True)
        ]
    )
    def test_is_notify_to_the_seller(self, shipment: Shipment, value) -> None:
        # Act
        result = shipment.is_notify_to_the_seller()

        # Assert
        assert result == value