from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    DomainError, 
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user import User


class PasswordChangeService:
    def __init__(
        self,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._password_hasher = password_hasher
    
    def change(
        self, 
        user: User, 
        password: str, 
        same_password: str
    ) -> None:
        if password != same_password:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)
        
        if user.email == password:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)

        return user.change_password(
            self._password_hasher.hash(password)
        ) 