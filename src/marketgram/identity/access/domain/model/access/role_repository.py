from typing import Protocol

from marketgram.identity.access.domain.model.access.role import Role


class RoleRepository(Protocol):
    async def add(self, role: Role) -> None:
        raise NotImplementedError