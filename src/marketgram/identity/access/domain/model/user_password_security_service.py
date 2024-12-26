from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_PASSWORD, 
    PasswordError
)


class UserPasswordSecurityService:
    def __init__(self) -> None:
        self._ph = PasswordHasher()
    
    def hash(self, plain_password: str) -> str:
        return self._ph.hash(plain_password)
    
    def verify(self, plain_password: str, hash_password: str) -> None:
        try:
            self._ph.verify(hash_password, plain_password)
            
        except (VerificationError, VerifyMismatchError):
            raise PasswordError(INVALID_PASSWORD)
        
    def lifetime_hash(self, hash_password: str) -> bool:
        return self._ph.check_needs_rehash(hash_password)