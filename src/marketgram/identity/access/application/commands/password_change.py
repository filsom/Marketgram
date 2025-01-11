from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.application.handler import Command
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)


@dataclass
class PasswordChangeCommand(Command):
    session_id: UUID
    old_password: str
    new_password: str


class PasswordChangeHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        web_session_repository: WebSessionRepository,
        password_hasher: PasswordHasher
    ) -> None:
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

        AuthenticationService(self._password_hasher) \
            .authenticate(user, command.old_password)

        user.change_password(command.new_password, self._password_hasher)

        return await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)