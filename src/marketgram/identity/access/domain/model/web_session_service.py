from datetime import datetime, timedelta
from uuid import UUID

from marketgram.identity.access.domain.model.exceptions import DomainError
from marketgram.identity.access.domain.model.web_session import (
    WebSession
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)


class WebSessionService:
    def __init__(
        self,
        max_age: timedelta,
        web_session_repository: WebSessionRepository
    ) -> None:
        self._max_age = max_age
        self._web_session_repository = web_session_repository

    async def init(
        self, 
        user_id: UUID, 
        session_id: UUID,
        current_time: datetime, 
        device: str
    ) -> dict[str, str]:
        await self._web_session_repository \
            .delete_this_device(
                user_id,
                device
            )
        web_session = WebSession(
            user_id,
            session_id,
            current_time,
            current_time + self._max_age,
            device
        )
        await self._web_session_repository.add(web_session)

        return web_session.for_browser()
    
    async def extend(
        self, 
        current_id: UUID, 
        new_id: UUID,
        current_time: datetime
    ) -> WebSession:
        web_session = await self._web_session_repository \
            .lively_with_id(
                current_id,
                current_time
            )
        if web_session is None:
            raise DomainError()

        web_session.extend_service_life(
            new_id,
            self._max_age,
            current_time
        )
        return web_session