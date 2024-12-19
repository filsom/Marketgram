from uuid import UUID

from fastapi import Request, Response

from marketgram.identity.access.port.adapter.exceptions import (
    ACCESS_DENIED, 
    Unauthorized
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_web_session_repository import (
    SQLAlchemyWebSessionRepository
)
    

class IdentityProvider:
    def __init__(
        self,
        request: Request,
        response: Response,
        web_session_repository: SQLAlchemyWebSessionRepository
    ) -> None:
        self._request = request
        self._response = response
        self._web_session_repository = web_session_repository

    def provided_id(self) -> UUID:
        return self._provided_id
    
    async def get_user_id(self) -> None:    
        session_id = self._request.cookies.get('s_id')
        if session_id is None:
            raise Unauthorized(ACCESS_DENIED)
        
        web_session = (
            await self._web_session_repository
            .lively_with_id(session_id)
        )
        if web_session is None:
            raise Unauthorized(ACCESS_DENIED)

        web_session.extend_service_life()
        
        self._provided_id = web_session.user_id

        return self._response.set_cookie(
            key='s_id',
            value=web_session.to_string_id(),
            expires=web_session.to_formatted_time(),
            httponly=True
        )