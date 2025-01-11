from dataclasses import dataclass
from datetime import UTC, datetime

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.web_session_factory import (
    WebSessionFactory
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
        auth_service: AuthenticationService,
        web_session_repository: WebSessionRepository,
    ) -> None:
        self._user_repository = user_repository
        self._auth_service = auth_service
        self._web_session_repository = web_session_repository

    async def handle(self, command: UserLoginCommand) -> dict[str, str]:
        user = await self._user_repository.with_email(command.email)
        if user is None:
            raise ApplicationError()
        
        self._auth_service.authenticate(user, command.password)
        
        await self._web_session_repository \
            .delete_this_device(user.user_id, command.device)       

        web_session = WebSessionFactory().create(
            user.user_id, datetime.now(UTC), command.device
        )
        await self._web_session_repository.add(web_session)

        return web_session.for_browser()