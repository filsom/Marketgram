from dataclasses import dataclass
from datetime import UTC, datetime

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
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
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
        context: IAMContext,
        users_repository: UsersRepository,
        roles_repository: RolesRepository,
        jwt_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender,
        password_hasher: PasswordHasher
    ) -> None:
        self._context = context
        self._users_repository = users_repository
        self._roles_repository = roles_repository
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._password_hasher = password_hasher
        
    async def execute(self, command: UserRegistrationCommand) -> None:
        user = await self._users_repository.with_email(command.email)
        if user is not None:
            raise ApplicationError()
        
        user = UserFactory(self._password_hasher) \
            .create(command.email, command.password)
        role = Role(user.user_id, Permission.USER)
    
        jwt_token = self._jwt_manager.encode(
            datetime.now(UTC),
            {'sub': user.to_string_id(), 'aud': 'user:activate'}
        )
        message = self._message_renderer.render(command.email, jwt_token)
        
        self._users_repository.add(user)
        self._roles_repository.add(role)

        await self._email_sender.send_message(message)

        return await self._context.save_changes()