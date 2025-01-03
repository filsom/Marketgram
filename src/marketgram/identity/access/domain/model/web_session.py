from datetime import datetime, timedelta
from uuid import UUID


class WebSession:
    FORMAT = '%a, %d %b %Y %H:%M:%S'

    def __init__(
        self,
        user_id: UUID,
        session_id: UUID,
        created_at: datetime,
        expires_in: timedelta,
        device: str
    ) -> None:
        self._user_id = user_id
        self._session_id = session_id
        self._created_at = created_at
        self._expires_in = expires_in
        self._device = device

    def extend_service_life(
        self, 
        new_id: UUID,
        max_age: timedelta,
        current_time: datetime
    ) -> None:
        difference = self._expires_in - current_time

        if difference.days <= 1:
            self._session_id = new_id
            self._created_at = current_time
            self._expires_in = current_time + max_age
    
    def to_formatted_time(self) -> str:
        return self._expires_in.strftime(self.FORMAT)
    
    def to_string_id(self) -> str:
        return str(self.session_id)

    def for_browser(self) -> dict[str, str]:
        return {
            'session_id': self.to_string_id(),
            'expires_in': self.to_formatted_time()
        }
    
    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def session_id(self) -> UUID:
        return self._session_id
    
    @property
    def expires_in(self) -> datetime:
        return self._expires_in
    
    @property
    def created_at(self) -> datetime:
        return self._created_at

    def __eq__(self, other: 'WebSession') -> bool:
        if not isinstance(other, WebSession):
            return False

        return self.session_id == other.session_id
    
    def __hash__(self) -> int:
        return hash(self.session_id)