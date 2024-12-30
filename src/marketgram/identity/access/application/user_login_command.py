from dataclasses import dataclass
from uuid import UUID

from marketgram.identity.access.domain.model.web_session import (
    WebSession
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)


@dataclass
class UserLoginCommand:
    email: str
    password: str
    device: str


class UserLoginHandler:
    def __init__(
        self,
        auth_service: UserAuthenticationService,
        web_session_repository: WebSessionRepository,
    ) -> None:
        self._auth_service = auth_service
        self._web_session_repository = web_session_repository

    async def handle(self, command: UserLoginCommand) -> UUID:
        authenticated_user = await self._auth_service.using_email(
            command.email,
            command.password
        )
        await self._web_session_repository \
            .delete_this_device(command.device)
        
        web_session = WebSession(
            authenticated_user.user_id,
            command.device,
        )
        await self._web_session_repository.add(web_session)

        return web_session.for_browser()               