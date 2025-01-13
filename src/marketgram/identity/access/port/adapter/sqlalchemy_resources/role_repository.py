from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.role import Role


class RoleRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    def add(self, role: Role) -> None:
        self._async_session.add(role)

    async def with_id(self, user_id: UUID) -> Role | None:
        stmt = select(Role).where(Role._user_id == user_id)
        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()