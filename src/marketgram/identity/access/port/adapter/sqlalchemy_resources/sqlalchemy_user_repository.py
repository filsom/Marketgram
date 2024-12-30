from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.user import User


class SQLAlchemyUserRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def next_identity(self) -> UUID:
        return uuid4()
    
    async def with_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User._user_id == user_id)
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def with_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User._email == email)
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def add(self, user: User) -> None:
        self._async_session.add(user)