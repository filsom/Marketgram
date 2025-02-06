from marketgram.trade.domain.model.errors import ReplacingItemError
from marketgram.trade.domain.model.events import (
    PurchasedCardWithAutoShipmentEvent, 
    SellerShippedReplacementWithAutoShipmentEvent
)
from marketgram.trade.domain.model.trade_item.cards_repository import CardsRepository
from marketgram.trade.domain.model.trade_item.file_storage import FileStorage
from marketgram.trade.port.adapter.event_dispatcher import EventDispatcher



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
            event.deal.deal_id,
            event.deal.qty_purchased
        )
        return await event.deal.confirm_shipment(
            event.occurred_at
        )


class AutoShipmentReplacementEventHandler:
    def __init__(
        self,
        cards_repository: CardsRepository,
        event_dispatcher: EventDispatcher,
        file_storage: FileStorage
    ) -> None:
        self._cards_repository = cards_repository
        self._event_dispatcher = event_dispatcher
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
        else:
            await self._file_storage.allocate(
                event.dispute.deal_id,
                event.qty_return
            )
        return await self._event_dispatcher.dispatch(
            card.events
        )