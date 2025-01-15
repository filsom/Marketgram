from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, delete, select

from marketgram.identity.access.domain.model.web_session import (
    WebSession
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)


class WebSessionRepository:
    def __init__(
        self,
        context: IAMContext
    ) -> None:
        self.session = context.session

    async def add(self, web_session: WebSession) -> None:
        self.session.add(web_session)
    
    async def delete_this_device(self, user_id: UUID, device: str) -> None:
        stmt = delete(WebSession).where(and_(
            WebSession.device == device,
            WebSession.user_id == user_id
        ))
        await self.session.execute(stmt)

    async def delete_with_id(self, session_id: UUID) -> None:
        stmt = delete(WebSession).where(WebSession.session_id == session_id)
        await self.session.execute(stmt)

    async def delete_all_with_user_id(self, user_id: UUID) -> None:
        stmt = delete(WebSession).where(WebSession.user_id == user_id)
        await self.session.execute(stmt)

    async def lively_with_id(self, session_id: UUID, current_time: datetime) -> WebSession | None:
        stmt = select(WebSession).where(and_(
            WebSession.session_id == session_id,
            WebSession.expires_in > current_time
        ))
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()