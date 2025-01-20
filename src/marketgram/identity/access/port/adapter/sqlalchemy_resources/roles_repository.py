from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.role import Role


class RolesRepository:
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self.session = session

    def add(self, role: Role) -> None:
        self.session.add(role)

    async def with_id(self, user_id: UUID) -> Role | None:
        stmt = select(Role).where(Role._user_id == user_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()