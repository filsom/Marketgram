from uuid import UUID

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    USER_NOT_ACTIVATED, 
    DomainError
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)


class UserAuthenticationService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    async def using_id(self, user_id: UUID, plain_password: str) -> User:
        user = await self._user_repository.with_id(user_id)
        
        return self._authenticate(user, plain_password)
    
    async def using_email(self, email: str, plain_password: str) -> User:
        user = await self._user_repository.with_email(email)
        
        return self._authenticate(user, plain_password)

    def _authenticate(self, user: User, plain_password: str) -> User:
        if user is None:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)
        
        if not user.is_active:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)
        
        if not self._password_hasher.verify(plain_password, user.password):
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)

        if self._password_hasher.check_needs_rehash(user.password):
            user.change_password(plain_password)

        return user