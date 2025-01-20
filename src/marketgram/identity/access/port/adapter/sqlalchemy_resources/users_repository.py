from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.user import User


class UsersRepository:
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self.session = session
    
    async def with_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User._user_id == user_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def with_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User._email == email)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    
    def add(self, user: User) -> None:
        self.session.add(user)