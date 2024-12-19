from typing import Protocol


class TokenManager(Protocol):
    def encode(self, payload: dict[str, str]):
        raise NotImplementedError
    
    def decode(self, token: str, audience: str):
        raise NotImplementedError
    
