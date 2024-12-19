from dataclasses import dataclass

from marketgram.identity.access.application.email_sender import EmailSender
from marketgram.identity.access.application.message_maker import EmailMessageMaker
from marketgram.identity.access.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.identity.email import Email
from marketgram.identity.access.domain.model.identity.user_repository import (
    UserRepository
)


@dataclass
class ForgotPasswordCommand:
    email: str


class ForgotPasswordHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        message_maker: EmailMessageMaker,
        email_sender: EmailSender
    ) -> None:
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager
        self._message_maker = message_maker
        self._email_sender = email_sender
    
    async def handle(self, command: ForgotPasswordCommand) -> None:
        exists_user = await self._user_repository \
            .active_with_email(Email(command.email))
        
        if exists_user is not None:
            jwt_token = self._jwt_manager.encode({
                'sub': exists_user.to_string_id(),
                'aud': 'user:password'
            })
            message = self._message_maker.make(
                jwt_token, 
                exists_user.email
            )
            return await self._email_sender.send_message(message)