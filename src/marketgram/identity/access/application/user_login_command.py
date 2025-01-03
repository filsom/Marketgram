from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.web_session_service import (
    WebSessionService
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
        web_session_service: WebSessionService
    ) -> None:
        self._auth_service = auth_service
        self._web_session_service = web_session_service

    async def handle(self, command: UserLoginCommand) -> dict[str, str]:
        authenticated_user = await self._auth_service \
            .using_email(command.email, command.password)
        
        return await self._web_session_service.init(
            authenticated_user.user_id,
            uuid4(),
            datetime.now(UTC),
            command.device
        )              