from marketgram.identity.access.domain.model.exceptions import (
    USER_NOT_ACTIVATED, 
    DomainError
)
from marketgram.identity.access.domain.model.user_password_security_service import (
    UserPasswordSecurityService
)
from marketgram.identity.access.domain.model.user import User


class UserAuthenticationService:
    def __init__(self) -> None:
        self._password_service = UserPasswordSecurityService()
    
    def authenticate(
            self,
            user: User,
            plain_password: str,
    ) -> None:
        if not user.is_active:
            raise DomainError(USER_NOT_ACTIVATED)
        
        self._password_service.verify(plain_password, user.password)

        if self._password_service.lifetime_hash(user.password):
            user.password = plain_password