from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    DomainError
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user import User


class AuthenticationService:
    def __init__(
        self,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._password_hasher = password_hasher
    
    def authenticate(self, user: User, plain_password: str) -> None:
        if not user.is_active:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)
        
        if not self._password_hasher.verify(plain_password, user.password):
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)

        if self._password_hasher.check_needs_rehash(user.password):
            user.change_password(plain_password, self._password_hasher)