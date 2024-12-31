from datetime import datetime
from typing import Protocol
from uuid import UUID

from marketgram.identity.access.domain.model.web_session import WebSession


class WebSessionRepository(Protocol):
    async def add(self, web_session: WebSession) -> None:
        raise NotImplementedError
    
    async def delete_this_device(
        self, 
        user_id: UUID, 
        device: str
    ) -> None:
        raise NotImplementedError

    async def delete_with_session_id(
        self, 
        session_id: UUID
    ) -> None:
        raise NotImplementedError

    async def delete_all_with_user_id(
        self, 
        user_id: UUID
    ) -> None:
        raise NotImplementedError

    async def with_session_id(
        self, 
        session_id: UUID
    ) -> WebSession | None:
        raise NotImplementedError
    
    async def lively_with_id(
        self, 
        session_id: UUID, 
        current_time: datetime
    ) -> WebSession | None:
        raise NotImplementedError