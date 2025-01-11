from dataclasses import dataclass
from typing import Protocol, TypeVar


@dataclass
class Command:
    pass


Cmd = TypeVar('Cmd', bound=Command, contravariant=True)
Res = TypeVar('Res', covariant=True)


class Handler(Protocol[Cmd, Res]):
    async def handle(self, command: Cmd) -> Res:
        raise NotImplementedError()