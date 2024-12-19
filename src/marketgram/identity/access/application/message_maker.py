from email.message import Message
from typing import Any, Protocol


class EmailMessageMaker(Protocol):
    def make(self, fields: Any, _for: str) -> Message:
        raise NotImplementedError