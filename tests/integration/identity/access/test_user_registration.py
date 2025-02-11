from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.identity.access.port.adapter.html_renderer import MessageRenderer
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestUserRegistrationHandler(IAMTestCase):
    async def test_user_registration(
        self,
        activate_msg_renderer: MessageRenderer[str]
    ) -> None:
        # Arrange
        await self.delete_all()
        
        password_hasher = Argon2PasswordHasher()
        email_sender = AsyncMock()
        email_sender.send_message = AsyncMock()

        # Act
        await self.execute(
            UserRegistrationCommand('Test@mail.ru', 'unprotected'),
            JwtTokenManager('secret'),
            activate_msg_renderer,
            email_sender,
            password_hasher
        )

        # Assert
        email_sender.send_message.assert_called_once()

        user_from_db = await self.query_user_with_email('test@mail.ru')
        role_from_db = await self.query_role(user_from_db.user_id)
        
        assert user_from_db is not None
        assert user_from_db.email == 'test@mail.ru'
        assert not user_from_db.is_active
        assert password_hasher.verify(user_from_db.password, 'unprotected')
        assert role_from_db.permission == Permission.USER

    async def execute(
        self, 
        command: UserRegistrationCommand, 
        jwt_token_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender, 
        password_hasher: PasswordHasher
    ) -> None:
        async with AsyncSession(self._engine) as session:
            handler = UserRegistrationHandler(
                session,
                jwt_token_manager,
                message_renderer,
                email_sender,
                password_hasher
            )
            return await handler.execute(command)