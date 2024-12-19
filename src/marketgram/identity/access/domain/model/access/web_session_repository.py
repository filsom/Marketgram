from typing import Protocol
from uuid import UUID

from marketgram.identity.access.domain.model.access.web_session import WebSession


class WebSessionRepository(Protocol):
    async def add(self, web_session: WebSession) -> None:
        raise NotImplementedError
    
    async def delete_this_device(self, device: str) -> None:
        raise NotImplementedError

    async def delete_with_session_id(self, session_id: UUID) -> None:
        raise NotImplementedError

    async def delete_all_with_user_id(self, user_id: UUID) -> None:
        raise NotImplementedError

    async def with_session_id(self, session_id: UUID) -> WebSession | None:
        raise NotImplementedError
