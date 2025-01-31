from datetime import datetime

from marketgram.common.application.exceptions import DomainError


INFINITY = 'infinity'


class Description:
    def __init__(
        self,
        name: str,
        body: str,
        set_in: datetime,
        archived_in: datetime | str,
        is_verify: bool,
        description_id: int = None
    ) -> None:
        self._description_id = description_id
        self._name = name
        self._body = body
        self._set_in = set_in
        self._archived_in = archived_in
        self._is_verify = is_verify

    def set(self) -> None:
        self._is_verify = True

    def archive(self, current_time: datetime) -> None:
        self._archived_in = current_time

    @property
    def archiving_time(self) -> datetime:
        if self._archived_in == INFINITY:
            return datetime.max
        else:
            return self._archived_in

    def __lt__(self, other: object) -> None:
        if not isinstance(other, Description):
            raise DomainError()

        return self.archiving_time < other.archiving_time
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Description):
            return False

        return self._description_id == other._description_id
    
    def __hash__(self) -> int:
        return hash(self._description_id)