from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Argon2PasswordHasher(PasswordHasher):
    def verify(self, hash: str, password: str) -> bool:
        try:
            return super().verify(hash, password)
        except VerifyMismatchError:
            return False