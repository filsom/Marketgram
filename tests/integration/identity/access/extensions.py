from typing import Self
from uuid import UUID

from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.web_session import WebSession


class WebSessionExtensions:
    def __init__(self, web_session: WebSession | None) -> None:
        self._web_session = web_session

    def should_exist(self) -> Self:
        assert self._web_session is not None
        return self
    
    def with_session_id(self, session_id: str) -> Self:
        assert self._web_session.to_string_id() == session_id
        return self

    def with_user_id(self, user_id: str) -> Self:
        assert str(self._web_session.user_id) == user_id
        return self
    
    def with_device(self, device: str) -> Self:
        assert self._web_session.device == device
        return self

    def with_service_life_of_up_to(self, expires_in: str) -> Self:
        assert self._web_session.to_formatted_time() == expires_in
        return self
    

class UserExtensions:
    def __init__(self, user: User | None) -> None:
        self._user = user

    @property
    def user_id(self) -> UUID:
        return self._user.user_id

    def should_exist(self) -> Self:
        assert self._user is not None
        return self

    def with_email(self, email: str) -> Self:
        assert self._user.email == email
        return self
    
    def not_activated(self) -> Self:
        assert not self._user.is_active
        return self
    
    def activated(self) -> Self:
        assert self._user.is_active
        return self
    
    def with_hashed_password(
        self, 
        password: str, 
        password_hasher: PasswordHasher
    ) -> Self:
        assert password_hasher.verify(self._user.password, password)
        return self