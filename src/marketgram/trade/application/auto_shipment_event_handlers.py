from marketgram.trade.domain.model.errors import ReplacingItemError
from marketgram.trade.domain.model.events import (
    PurchasedCardWithAutoShipmentEvent, 
    SellerShippedReplacementWithAutoShipmentEvent
)
from marketgram.trade.port.adapter.file_storage import FileStorage
from marketgram.trade.port.adapter.sqlalchemy_resources.cards_repository import (
    CardsRepository
)


class AutoShipmentEventHandler:
    def __init__(
        self,
        file_storage: FileStorage
    ) -> None:
        self._file_storage = file_storage

    async def execute(
        self, 
        event: PurchasedCardWithAutoShipmentEvent
    ) -> None:
        await self._file_storage.allocate(
            event.deal.deal_id
        )
        return await event.deal.confirm_shipment(
            event.occurred_at
        )


class AutoReplacementEventHandler:
    def __init__(
        self,
        cards_repository: CardsRepository,
        file_storage: FileStorage
    ) -> None:
        self._cards_repository = cards_repository
        self._file_storage = file_storage

    async def execute(
        self, 
        event: SellerShippedReplacementWithAutoShipmentEvent
    ) -> None:
        card = await self._cards_repository \
            .sell_card_with_id(event.dispute.card_id)
        
        try:
            card.replace(event.qty_return, event.occurred_at)
        except ReplacingItemError:
            event.dispute.open_again()

        return await self._file_storage(event.dispute.deal_id)