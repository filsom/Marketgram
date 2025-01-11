from typing import Protocol


class PasswordSecurityHasher(Protocol):
    def hash(self, password: str) -> str:
        raise NotImplementedError
    
    def verify(self, hash: str, password: str) -> bool:
        raise NotImplementedError
    
    def check_needs_rehash(self, hash: str) -> bool:
        raise NotImplementedError