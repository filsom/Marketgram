import jwt

from datetime import datetime, timedelta
from uuid import UUID

from marketgram.identity.access.port.adapter.exceptions import (
    JWT_ERROR, 
    JWTVerifyException
)


class JwtTokenManager:
    MIN = 15
    ALGORITHM = 'HS256'

    def __init__(self, secret: str) -> None:
        self._secret = secret

    def encode(
        self, 
        current_time: datetime, 
        payload: dict[str, str]
    ) -> str:
        payload['exp'] = current_time + timedelta(minutes=self.MIN)

        return jwt.encode(payload, self._secret, algorithm=self.ALGORITHM)
    
    def decode(self, token: str, audience: str) -> UUID:
        try:
            payload = jwt.decode(
                token, 
                key=self._secret, 
                audience=audience, 
                algorithms=[self.ALGORITHM]
            )
        except jwt.PyJWTError:
            raise JWTVerifyException(JWT_ERROR) 
        
        return UUID(payload['sub'])