from unittest.mock import AsyncMock, Mock

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.application.commands.forgot_password import (
    ForgotPasswordCommand, 
    ForgotPasswordHandler
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.settings import ForgotPasswordHtmlSettings
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestForgotPasswordHandler(IAMTestCase):
    async def test_forgot_password(
        self,
        forgot_password_msg_renderer: MessageRenderer[ForgotPasswordHtmlSettings, str]
    ) -> None:
        # Arrange
        await self.create_user()

        email_sender = AsyncMock()
        email_sender.send_message = AsyncMock()

        # Act
        await self.execute(
            ForgotPasswordCommand('test@mail.ru'),
            JwtTokenManager('secret'),
            Mock(),
            email_sender
        )

        # Assert 
        email_sender.send_message.assert_called_once()

    async def execute(
        self,
        command: ForgotPasswordCommand,
        token_manager: JwtTokenManager,
        message_renderer: MessageRenderer,
        email_sender: EmailSender
    ) -> None:
        async with AsyncSession(self.engine) as session:
            await session.begin()
            handler = ForgotPasswordHandler(
                IAMContext(session),
                token_manager,
                message_renderer,
                email_sender
            )
            return await handler.execute(command)