import jwt

from datetime import datetime, timedelta, timezone
from uuid import UUID

from marketgram.identity.access.port.adapter.exceptions import (
    JWT_ERROR, 
    JWTVerifyException

)
from marketgram.identity.access.settings import JWTManagerSecret

class JwtTokenManager:
    def __init__(
        self,
        secret: JWTManagerSecret,
    ) -> None:
        self._secret = secret

    def encode(self, payload: dict[str, str]) -> str:
        exp = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
        payload['exp'] = exp

        return jwt.encode(
            payload, 
            self._secret.secret, 
            algorithm='HS256'
        )
    
    def decode(self, token: str, audience: str):
        try:
            payload = jwt.decode(
                token, 
                key=self._secret.secret, 
                audience=audience, 
                algorithms=['HS256']
            )

        except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError):
            raise JWTVerifyException(JWT_ERROR)
        
        return UUID(payload['sub'])