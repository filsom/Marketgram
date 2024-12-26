from typing import Protocol


class IdProvider(Protocol):
    def provided_id(self):
        raise NotImplementedError
    
    async def get_user_id(self):
        raise NotImplementedError