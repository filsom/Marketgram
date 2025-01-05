from dataclasses import dataclass

from marketgram.common.application.handler import Handler
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.user_creation_service import (
    UserCreationService
)
from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import ContentFields, MessageRenderer


@dataclass
class UserRegistrationCommand:
    email: str
    password: str
    same_password: str


@dataclass
class ActivationToken(ContentFields):
    value: str


class UserRegistration(
    Handler[UserRegistrationCommand, None]
):
    def __init__(
        self,
        user_creation_service: UserCreationService,
        jwt_manager: TokenManager,
        message_renderer: MessageRenderer[ActivationToken],
        email_sender: EmailSender
    ) -> None:
        self._user_creation_service = user_creation_service
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        
    async def handle(self, command: UserRegistrationCommand) -> None:
        user_id = await self._user_creation_service.create(
            command.email,
            command.password,
            command.same_password
        )
        jwt_token = self._jwt_manager.encode({
            'sub': user_id,
            'aud': 'user:activate'
        })
        message = self._message_renderer.render(
            command.email,
            ActivationToken(jwt_token)
        )
        return await self._email_sender.send_message(message)