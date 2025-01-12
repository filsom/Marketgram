from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.domain.model.role import Role


class RoleRepository:
    def __init__(
        self,
        async_session: AsyncSession
    ) -> None:
        self._async_session = async_session

    async def add(self, role: Role) -> None:
        self._async_session.add(role)