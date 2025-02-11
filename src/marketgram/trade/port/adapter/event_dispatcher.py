from marketgram.common.entity import DomainEvent, IntegrationEvent


class EventDispatcher:
    async def dispatch(
        self, 
        *events: list[DomainEvent | IntegrationEvent]
    ) -> None:
        pass