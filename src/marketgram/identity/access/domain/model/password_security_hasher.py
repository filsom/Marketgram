from typing import Protocol


class PasswordSecurityHasher(Protocol):
    def hash(self, password: str) -> str:
        raise NotImplementedError
    
    def verify(self, hash_password: str, password: str) -> bool:
        raise NotImplementedError
    
    def check_needs_rehash(hash: str) -> bool:
        raise NotImplementedError