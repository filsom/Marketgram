from datetime import datetime, timedelta
from uuid import UUID, uuid4


class WebSession:
    MAX_AGE_DAYS = 15
    FORMAT = '%a, %d %b %Y %H:%M:%S'

    def __init__(
        self,
        user_id: UUID,
        device: str,
    ) -> None:
        self._user_id = user_id
        self._device = device
        self._session_id = uuid4()
        self._created_at = datetime.now()
        self._expires_in = self._created_at + timedelta(
            days=self.MAX_AGE_DAYS
        )
        self._device = device

    def extend_service_life(self) -> None:
        current_date = datetime.now()
        if self._day_difference(current_date) <= 1:
            self._refresh(current_date)
    
    def to_formatted_time(self) -> str:
        return self._expires_in.strftime(
            self.FORMAT
        )
    
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

    def _day_difference(self, current_date: datetime) -> int:
        difference = self._expires_in - current_date
        return difference.days

    def _refresh(self, current_date: datetime) -> None:
        self._session_id = uuid4()
        self._created_at = current_date
        self._expires_in = current_date + timedelta(
            days=self.MAX_AGE_DAYS
        )

    def __eq__(self, other: 'WebSession') -> bool:
        if not isinstance(other, WebSession):
            return False

        return self.session_id == other.session_id
    
    def __hash__(self) -> int:
        return hash(self.session_id)