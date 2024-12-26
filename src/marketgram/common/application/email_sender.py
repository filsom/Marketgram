from email.message import Message
from typing import Protocol


class EmailSender(Protocol):
    async def send_message(self, message: Message) -> None:
        raise NotImplementedError