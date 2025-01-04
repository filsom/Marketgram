from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)


@dataclass
class ChangePasswordCommand:
    session_id: UUID
    old_password: str
    new_password: str
    same_password: str


class ChangePasswordHandler:
    def __init__(
        self,
        auth_service: UserAuthenticationService,
        password_service: PasswordChangeService,
        web_session_repository: WebSessionRepository
    ) -> None:
        self._auth_service = auth_service
        self._password_service = password_service
        self._web_session_repository = web_session_repository

    async def handle(self, command: ChangePasswordCommand) -> None:
        web_session = await self._web_session_repository \
            .lively_with_id(
                command.session_id,
                datetime.now(UTC)
            )
        if web_session is None:
            raise ApplicationError()
        
        authenticated_user = await self._auth_service.using_id(
            web_session.user_id,
            command.old_password
        )
        self._password_service.change(
            authenticated_user,
            command.new_password,
            command.same_password
        )
        return await self._web_session_repository \
            .delete_all_with_user_id(authenticated_user.user_id)