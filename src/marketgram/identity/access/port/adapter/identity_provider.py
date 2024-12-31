from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import Request, Response

from marketgram.identity.access.domain.model.exceptions import DomainError
from marketgram.identity.access.domain.model.web_session_service import WebSessionService
from marketgram.identity.access.port.adapter.exceptions import (
    ACCESS_DENIED, 
    Unauthorized
)
    

class IdentityProvider:
    def __init__(
        self,
        request: Request,
        response: Response,
        web_session_service: WebSessionService
    ) -> None:
        self._request = request
        self._response = response
        self._web_session_service = web_session_service

    def provided_id(self) -> UUID:
        return self._provided_id
    
    async def get_user_id(self) -> None:    
        session_id = self._request.cookies.get('s_id')
        if session_id is None:
            raise Unauthorized(ACCESS_DENIED)
        
        try:
            web_session = await self._web_session_service.extend(
                session_id,
                uuid4(),
                datetime.now(UTC)
            )
            details = web_session.for_browser()
        except DomainError:
            raise Unauthorized(ACCESS_DENIED)
        
        self._provided_id = web_session.user_id

        return self._response.set_cookie(
            key='s_id',
            value=details['session_id'],
            expires=details['expires_in'],
            httponly=True
        )