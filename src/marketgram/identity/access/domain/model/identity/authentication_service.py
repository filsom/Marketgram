from marketgram.identity.access.domain.model.exceptions import (
    USER_NOT_ACTIVATED, 
    DomainException
)
from marketgram.identity.access.domain.model.identity.password_service import (
    PasswordService
)
from marketgram.identity.access.domain.model.identity.user import User


class AuthenticationService:
    def __init__(self) -> None:
        self._password_service = PasswordService()
    
    def authenticate(
            self,
            user: User,
            plain_password: str,
    ) -> None:
        if not user.is_active:
            raise DomainException(USER_NOT_ACTIVATED)
        
        self._password_service.verify(plain_password, user.password)

        if self._password_service.lifetime_hash(user.password):
            user.password = plain_password