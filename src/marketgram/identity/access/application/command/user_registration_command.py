from dataclasses import dataclass

from marketgram.identity.access.application.jwt_manager import TokenManager
from marketgram.identity.access.application.exceptions import (
    ApplicationException, 
)
from marketgram.identity.access.domain.model.access.role import Role
from marketgram.identity.access.domain.model.access.role_permission import (
    Permission
)
from marketgram.identity.access.domain.model.access.role_repository import (
    RoleRepository
)
from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD
)
from marketgram.identity.access.domain.model.identity.email import Email
from marketgram.identity.access.domain.model.identity.user import User
from marketgram.identity.access.domain.model.identity.user_repository import (
    UserRepository
)
from marketgram.identity.access.application.email_sender import EmailSender
from marketgram.identity.access.application.message_maker import EmailMessageMaker


@dataclass
class UserRegistrationCommand:
    email: str
    password: str
    same_password: str


class UserRegistrationHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        jwt_manager: TokenManager,
        message_maker: EmailMessageMaker,
        email_sender: EmailSender
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._jwt_manager = jwt_manager
        self._message_maker = message_maker
        self._email_sender = email_sender
        
    async def handle(self, command: UserRegistrationCommand) -> None:
        exists_user = await self._user_repository \
            .with_email(Email(command.email))
        
        if exists_user is not None:
            raise ApplicationException(INVALID_EMAIL_OR_PASSWORD)
        
        new_user = User(
            self._user_repository.next_identity(),
            Email(command.email),
            command.password
        )
        role_for_user = Role(
            new_user.user_id,
            Permission.USER
        )
        await self._user_repository.add(new_user)
        await self._role_repository.add(role_for_user)

        jwt_token = self._jwt_manager.encode({
            'sub': new_user.to_string_id(),
            'aud': 'user:activate'
        })
        message = self._message_maker.make(
            jwt_token, 
            new_user.email
        )
        return await self._email_sender.send_message(message)