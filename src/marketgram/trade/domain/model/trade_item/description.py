from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from marketgram.trade.domain.model.types import INFINITY


class StatusDescription(StrEnum):
    NEW = auto()
    CURRENT = auto()
    ARCHIVED = auto()
    CANCELLED = auto()


class Description:
    def __init__(
        self,
        card_id: UUID,
        name: str,
        body: str,
        status: StatusDescription,
        description_id: int = None,
        set_in: datetime = None,
        archived_in: datetime | str = INFINITY
    ) -> None:
        self._card_id = card_id
        self._description_id = description_id
        self._name = name
        self._body = body
        self._status = status
        self._set_in = set_in
        self._archived_in = archived_in

    def set(self, current_time: datetime) -> None:
        self._set_in = current_time
        self._status = StatusDescription.CURRENT

    def archive(self, current_time: datetime) -> None:
        self._archived_in = current_time
        self._status = StatusDescription.ARCHIVED

    def cancel(self) -> None:
        self._status = StatusDescription.CANCELLED
        
    @property
    def status(self) -> StatusDescription:
        return self._status
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Description):
            return False

        return self._description_id == other._description_id
    
    def __hash__(self) -> int:
        return hash(self._description_id)