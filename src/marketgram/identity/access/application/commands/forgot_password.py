from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)


@dataclass
class ForgotPasswordCommand:
    email: str


class ForgotPasswordHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._users_repository = UsersRepository(session)
    
    async def execute(self, command: ForgotPasswordCommand) -> None:
        async with self._session.begin():
            user = await self._users_repository.with_email(command.email) 
            if user is None or not user.is_active:
                return 
            
            jwt_token = self._jwt_manager.encode(
                datetime.now(UTC),
                {'sub': user.to_string_id(), 'aud': 'user:password'}
            )
            message = self._message_renderer.render(user.email, jwt_token)
            await self._email_sender.send_message(message)
            
            await self._session.commit()