from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.domain.model.role_repository import RoleRepository
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.settings import ActivateHtmlSettings


@dataclass
class UserRegistrationCommand:
    email: str
    password: str


class UserRegistrationHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        user_factory: UserFactory,
        jwt_manager: TokenManager,
        message_renderer: MessageRenderer[
            ActivateHtmlSettings, str
        ],
        email_sender: EmailSender,
        password_hasher: PasswordHasher
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._user_factory= user_factory
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._password_hasher = password_hasher
        
    async def handle(self, command: UserRegistrationCommand) -> None:
        user = await self._user_repository.with_email(command.email)
        if user is not None:
            raise ApplicationError()
        
        user = UserFactory(self._password_hasher) \
            .create(command.email, command.password)
        role = Role(user.user_id, Permission.USER)

        jwt_token = self._jwt_manager.encode({
            'sub': user.to_string_id(),
            'aud': 'user:activate'
        })
        message = self._message_renderer.render(command.email, jwt_token)
        
        await self._user_repository.add(user)
        await self._role_repository.add(role)

        return await self._email_sender.send_message(message)