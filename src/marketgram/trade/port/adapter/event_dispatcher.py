from marketgram.common.domain.model.entity import DomainEvent, IntegrationEvent


class EventDispatcher:
    async def dispatch(
        self, 
        events: list[DomainEvent | IntegrationEvent]
    ) -> None:
        pass