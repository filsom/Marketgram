from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.roles_repository import (
    RolesRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)


@dataclass
class UserRegistrationCommand:
    email: str
    password: str
    

class UserRegistrationHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._roles_repository = RolesRepository(session)
        
    async def execute(self, command: UserRegistrationCommand) -> None:
        async with self._session.begin():
            user = await self._users_repository.with_email(command.email)
            if user is not None:
                raise ApplicationError()
            
            new_user = UserFactory(self._password_hasher) \
                .create(command.email, command.password)
            role = Role(new_user.user_id, Permission.USER)

            self._users_repository.add(new_user)
            self._roles_repository.add(role)
            
            jwt_token = self._jwt_manager.encode(
                datetime.now(UTC),
                {'sub': new_user.to_string_id(), 'aud': 'user:activate'}
            )
            message = self._message_renderer.render(command.email, jwt_token)
            await self._email_sender.send_message(message)

            await self._session.commit()