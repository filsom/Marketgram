from uuid import UUID

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    PasswordError,
)
from marketgram.identity.access.domain.model.user_password_security_service import (
    UserPasswordSecurityService
)


class User:
    def __init__(
        self,
        user_id: UUID,
        email: str,
        password: str,
        is_active: bool = False
    ) -> None:
        self._user_id = user_id
        self._email = email
        self._is_active = is_active
        self.password = password

    def activate(self) -> None:
        self._is_active = True
        
    def to_string_id(self) -> str:
        return str(self._user_id)
    
    @property
    def user_id(self) -> UUID:
        return self._user_id
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, password: str) -> None:
        if self._email == password:
            raise PasswordError(INVALID_EMAIL_OR_PASSWORD)

        self._password = UserPasswordSecurityService().hash(password)
        
    def __eq__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return False

        return self.user_id == other.user_id
    
    def __hash__(self) -> int:
        return hash(self.user_id)