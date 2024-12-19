from typing import Optional, Protocol
from uuid import UUID

from marketgram.identity.access.domain.model.identity.email import Email
from marketgram.identity.access.domain.model.identity.user import User


class UserRepository(Protocol):
    def next_identity(self) -> UUID:
        raise NotImplementedError
    
    async def with_id(self, user_id: UUID) -> Optional[User]:
        raise NotImplementedError
    
    async def with_email(self, email: Email) -> Optional[User]:
        raise NotImplementedError
    
    async def add(self, user: User) -> None:
        raise NotImplementedError
    
    async def active_with_email(self, email: Email) -> Optional[User]:
        raise NotImplementedError