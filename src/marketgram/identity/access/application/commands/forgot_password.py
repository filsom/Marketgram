from dataclasses import dataclass

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.handler import Handler
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)


@dataclass
class ForgottenPasswordCommand:
    email: str


@dataclass
class PasswordChangeToken:
    value: str


class ForgottenPassword(
    Handler[ForgottenPasswordCommand, None]
):
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        message_renderer: MessageRenderer[PasswordChangeToken],
        email_sender: EmailSender
    ) -> None:
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
    
    async def handle(self, command: ForgottenPasswordCommand) -> None:
        user = await self._user_repository.with_email(command.email)
        
        if user is not None and user.is_active:
            jwt_token = self._jwt_manager.encode({
                'sub': user.to_string_id(),
                'aud': 'user:password'
            })
            message = self._message_renderer.render(
                user.email,
                PasswordChangeToken(jwt_token) 
            )
            return await self._email_sender.send_message(message)