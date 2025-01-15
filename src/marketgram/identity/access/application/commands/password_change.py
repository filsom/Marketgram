from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)


@dataclass
class PasswordChangeCommand:
    session_id: UUID
    old_password: str
    new_password: str


class PasswordChangeHandler:
    def __init__(
        self,
        context: IAMContext,
        password_hasher: PasswordHasher
    ) -> None:
        self._context = context
        self._user_repository = UserRepository(context)
        self._web_session_repository = WebSessionRepository(context)
        self._password_hasher = password_hasher

    async def execute(self, command: PasswordChangeCommand) -> None:
        web_session = await self._web_session_repository.lively_with_id(
            command.session_id, datetime.now()
        )
        if web_session is None:
            raise ApplicationError()
        
        user = await self._user_repository.with_id(web_session.user_id)

        AuthenticationService(self._password_hasher) \
            .authenticate(user, command.old_password)

        user.change_password(command.new_password, self._password_hasher)

        await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)
        
        await self._context.save_changes()