from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.application.commands.forgot_password import ForgotPasswordCommand, ForgotPasswordHandler
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import UserRepository
from marketgram.identity.access.settings import ForgotPasswordHtmlSettings, JWTManagerSecret


async def test_forgot_password(
    engine: AsyncGenerator[AsyncEngine, None], 
    forgot_password_msg_renderer: MessageRenderer[ForgotPasswordHtmlSettings, str]
) -> None:
    # Arrange
    email = 'test@mail.ru'

    email_sender = AsyncMock()

    async with AsyncSession(engine) as session:
        await session.begin()
        user = User(
            uuid4(),
            email,
            Argon2PasswordHasher().hash('protected')
        )
        user.activate()

        session.add(user)
        await session.commit()

    async with AsyncSession(engine) as session:
        await session.begin()
        sut = ForgotPasswordHandler(
            UserRepository(session),
            JwtTokenManager(JWTManagerSecret('secret')),
            Mock(),
            email_sender
        )

    # Act
        await sut.handle(ForgotPasswordCommand(email))

    # Assert 
    sut._email_sender.send_message.assert_called_once()