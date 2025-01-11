from marketgram.identity.access.domain.model.errors import (
    INVALID_EMAIL_OR_PASSWORD,
    PersonalDataError
)
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.domain.model.user import User


class AuthenticationService:
    def __init__(
        self,
        password_hasher: PasswordHasher
    ) -> None:
        self._password_hasher = password_hasher
    
    def authenticate(self, user: User, plain_password: str) -> None:
        if not user.is_active:
            raise PersonalDataError(INVALID_EMAIL_OR_PASSWORD)
        
        if not self._password_hasher.verify(user.password, plain_password):
            raise PersonalDataError(INVALID_EMAIL_OR_PASSWORD)

        if self._password_hasher.check_needs_rehash(user.password):
            user.change_password(plain_password, self._password_hasher)