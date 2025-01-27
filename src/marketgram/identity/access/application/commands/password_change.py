from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_sessions_repository import (
    WebSessionsRepository
)


@dataclass
class PasswordChangeCommand:
    session_id: UUID
    old_password: str
    new_password: str


class PasswordChangeHandler:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._web_sessions_repository = WebSessionsRepository(session)

    async def execute(self, command: PasswordChangeCommand) -> None:
        await self._session.begin()
        web_session = await self._web_sessions_repository \
            .lively_with_id(command.session_id, datetime.now())
        
        if web_session is None:
            raise ApplicationError()
        
        user = await self._users_repository.with_id(web_session.user_id)

        AuthenticationService(self._password_hasher) \
            .authenticate(user, command.old_password)

        user.change_password(command.new_password, self._password_hasher)

        await self._web_sessions_repository \
            .delete_all_with_user_id(user.user_id)
        
        await self._session.commit()