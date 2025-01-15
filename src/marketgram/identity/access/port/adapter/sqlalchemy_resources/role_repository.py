from uuid import UUID
from sqlalchemy import select

from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)


class RoleRepository:
    def __init__(
        self,
        session: IAMContext
    ) -> None:
        self.session = session.session

    def add(self, role: Role) -> None:
        self.session.add(role)

    async def with_id(self, user_id: UUID) -> Role | None:
        stmt = select(Role).where(Role._user_id == user_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()