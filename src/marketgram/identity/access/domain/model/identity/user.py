from uuid import UUID

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    PasswordException,
)
from marketgram.identity.access.domain.model.identity.email import Email
from marketgram.identity.access.domain.model.identity.password_service import (
    PasswordService
)


class User:
    def __init__(
        self,
        user_id: UUID,
        email: Email,
        password: str
    ) -> None:
        self._user_id = user_id
        self._email = email
        self._password = password
        self._is_active: bool = False

    def activate(self) -> None:
        self._is_active = True
        
    def to_string_id(self) -> str:
        return str(self._user_id)
    
    @property
    def user_id(self) -> UUID:
        return self._user_id
    
    @property
    def email(self) -> Email:
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
            raise PasswordException(INVALID_EMAIL_OR_PASSWORD)

        self._password = PasswordService().hash(password)
        
    def __eq__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return False

        return self.user_id == other.user_id
    
    def __hash__(self) -> int:
        return hash(self.user_id)