from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, select

from marketgram.identity.access.domain.model.web_session import (
    WebSession
)


class SQLAlchemyWebSessionRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    async def add(self, web_session: WebSession) -> None:
        self._async_session.add(web_session)
    
    async def delete_this_device(self, user_id: UUID, device: str) -> None:
        stmt = delete(WebSession).where(and_(
            WebSession._device == device,
            WebSession._user_id == user_id
        ))
        await self._async_session.execute(stmt)

    async def delete_with_id(self, session_id: UUID) -> None:
        stmt = delete(WebSession).where(WebSession._session_id == session_id)
        await self._async_session.execute(stmt)

    async def delete_all_with_user_id(self, user_id: UUID) -> None:
        stmt = delete(WebSession).where(WebSession._user_id == user_id)
        await self._async_session.execute(stmt)

    async def lively_with_id(self, session_id: UUID, current_time: datetime) -> WebSession | None:
        stmt = select(WebSession).where(and_(
            WebSession._session_id == session_id,
            WebSession._expires_in > current_time
        ))
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()