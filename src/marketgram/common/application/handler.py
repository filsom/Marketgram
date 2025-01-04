from typing import Generic, TypeVar


Cmd = TypeVar('Cmd')
Res = TypeVar('Res')


class Handler(Generic[Cmd, Res]):
    async def handle(self, command: Cmd) -> Res:
        raise NotImplementedError()