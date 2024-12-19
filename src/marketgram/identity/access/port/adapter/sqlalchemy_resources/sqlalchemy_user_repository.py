from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.identity.email import Email
from marketgram.identity.access.domain.model.identity.user import User


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

    async def with_email(self, email: Email) -> Optional[User]:
        stmt = select(User).where(User._email == email)
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def active_with_email(self, email: Email) -> Optional[User]:
        stmt = select(User).where(and_(
            User._email == email,
            User._is_active == True
        ))
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def add(self, user: User) -> None:
        self._async_session.add(user)