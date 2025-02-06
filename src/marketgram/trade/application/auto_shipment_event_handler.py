from marketgram.trade.domain.model.events import PurchasedCardWithAutoShipmentEvent
from marketgram.trade.port.adapter.file_storage import FileStorage


class AutoShipmentEventHandler:
    def __init__(
        self,
        file_storage: FileStorage
    ) -> None:
        self._file_storage = file_storage

    async def execute(self, event: PurchasedCardWithAutoShipmentEvent) -> None:
        await self._file_storage.allocate(
            event.deal.deal_id
        )
        await event.deal.confirm_shipment(
            event.occurred_at
        )