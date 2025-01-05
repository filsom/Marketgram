from uuid import UUID

from marketgram.identity.access.domain.model.exceptions import (
    DomainError
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
        self._password = password
        self._is_active = is_active

    def change_password(self, password: str) -> None:
        if not self._is_active:
            raise DomainError()
        
        self._password = password

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
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return self.user_id == other.user_id
    
    def __hash__(self) -> int:
        return hash(self.user_id)