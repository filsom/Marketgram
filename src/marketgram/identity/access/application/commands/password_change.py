from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)


@dataclass
class PasswordChangeCommand:
    session_id: UUID
    old_password: str
    new_password: str


class PasswordChangeHandler:
    def __init__(
        self,
        auth_service: AuthenticationService,
        user_repository: UserRepository,
        web_session_repository: WebSessionRepository,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._auth_service = auth_service
        self._user_repository = user_repository
        self._web_session_repository = web_session_repository
        self._password_hasher = password_hasher

    async def handle(self, command: PasswordChangeCommand) -> None:
        web_session = await self._web_session_repository.lively_with_id(
            command.session_id, datetime.now(UTC)
        )
        if web_session is None:
            raise ApplicationError()
        
        user = await self._user_repository.with_id(web_session.user_id)

        self._auth_service.authenticate(user, command.old_password)

        user.change_password(command.new_password, self._password_hasher)

        return await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)