from uuid import uuid4

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD, 
    DomainError,
    PersonalDataError
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user import User
    

class UserFactory:
    def __init__(
        self,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._password_hasher = password_hasher

    def create(self, email: str, password: str) -> User:
        if email == password:
            raise PersonalDataError(INVALID_EMAIL_OR_PASSWORD)

        return User(
            uuid4(),
            email.lower(),
            self._password_hasher.hash(password)
        )