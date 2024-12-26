from dataclasses import dataclass
from uuid import UUID

from marketgram.common.application.exceptions import (
    ApplicationError
)
from marketgram.identity.access.domain.model.web_session import (
    WebSession
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD
)
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)


@dataclass
class UserLoginCommand:
    email: str
    password: str
    device: str


class UserLoginHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        web_session_repository: WebSessionRepository,
    ) -> None:
        self._user_repository = user_repository
        self._web_session_repository = web_session_repository

    async def handle(self, command: UserLoginCommand) -> UUID:
        exists_user = await self._user_repository \
            .active_with_email(command.email)
        
        if exists_user is None:
            raise ApplicationError(INVALID_EMAIL_OR_PASSWORD)
        
        UserAuthenticationService().authenticate(
            exists_user,
            command.password,
        )
        await self._web_session_repository \
            .delete_this_device(command.device)
        
        web_session = WebSession(
            exists_user.user_id,
            command.device,
        )
        await self._web_session_repository.add(web_session)

        return web_session.for_browser()               