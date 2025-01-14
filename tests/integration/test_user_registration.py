from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.role_repository import (
    RoleRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.settings import (
    ActivateHtmlSettings, 
    JWTManagerSecret
)
from tests.integration.base import IAMTestCase


class TestUserRegistrationHandler(IAMTestCase):
    async def test_user_registration(
        self,
        activate_msg_renderer: MessageRenderer[ActivateHtmlSettings, str]
    ) -> None:
        # Arrange
        password_hasher = Argon2PasswordHasher()
        email_sender = AsyncMock()
        email_sender.send_message = AsyncMock()

        # Act
        await self.execute(
            UserRegistrationCommand('test@mail.ru', 'unprotected'),
            JwtTokenManager(JWTManagerSecret('secret')),
            activate_msg_renderer,
            email_sender,
            password_hasher
        )

        # Assert
        email_sender.send_message.assert_called_once()

        user = await self.query_user_with_email('test@mail.ru')
        user \
            .should_existing() \
            .with_email('test@mail.ru') \
            .email_is_lower() \
            .not_activated() \
            .with_hashed_password('unprotected', password_hasher)
        
        role = await self.query_role(user.user_id)
        assert role.permission == Permission.USER

    async def execute(
        self, 
        command: UserRegistrationCommand, 
        jwt_token_manager: JwtTokenManager,
        message_renderer: MessageRenderer[ActivateHtmlSettings, str],
        email_sender: EmailSender, 
        password_hasher: Argon2PasswordHasher
    ) -> None:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            sut = UserRegistrationHandler(
                IAMContext(session),
                UserRepository(session),
                RoleRepository(session),
                jwt_token_manager,
                message_renderer,
                email_sender,
                password_hasher
            )
            return await sut.execute(command)