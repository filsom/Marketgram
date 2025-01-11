from typing import Optional, Protocol
from uuid import UUID

from marketgram.identity.access.domain.model.user import User


class UserRepository(Protocol):
    async def with_id(self, user_id: UUID) -> Optional[User]:
        raise NotImplementedError
    
    async def with_email(self, email: str) -> Optional[User]:
        raise NotImplementedError
    
    async def add(self, user: User) -> None:
        raise NotImplementedError