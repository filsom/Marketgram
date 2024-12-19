from dataclasses import dataclass
from hashlib import sha256
from hmac import new, compare_digest

from marketgram.identity.access.port.adapter.exceptions import UNKNOWN_VALUE, AnalysisErrorHMAC


@dataclass
class SecretEncrypterHMAC:
    value: str


class EncrypterHMAC:
    def __init__(
        self,
        secret: SecretEncrypterHMAC
    ) -> None:
        self._secret = secret

    def encrypt(self, value: str) -> str:
        encrypt_value = new(
            self._secret.value.encode(),
            value.encode(),
            sha256,
        ).hexdigest()

        return encrypt_value
    
    def validate(self, hmac_value: str, audit_value: str) -> None:
        encrypt_value = self.encrypt(audit_value)

        if not compare_digest(encrypt_value, hmac_value):
            raise AnalysisErrorHMAC(UNKNOWN_VALUE)