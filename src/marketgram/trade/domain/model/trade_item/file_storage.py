from typing import Protocol


class FileStorage(Protocol):
    async def allocate(self, deal_id: int, quantity: int) -> None:
        raise NotImplementedError