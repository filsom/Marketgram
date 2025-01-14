from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)
from tests.integration.base import IAMTestCase
                

class TestUserLoginHandler(IAMTestCase):
    async def test_user_login(self) -> None:
        # Arrange
        user = await self.create_user()

        # Act
        result = await self.execute(
            UserLoginCommand('test@mail.ru', 'protected', 'Nokia 3210')
        )

        # Assert
        web_session_from_db = await self.query_web_session(
            UUID(result['session_id'])
        )
        web_session_from_db \
            .should_existing() \
            .with_user_id(user.user_id) \
            .with_session_id(result['session_id']) \
            .with_device('Nokia 3210') \
            .with_service_life_of_up_to(result['expires_in'])

    async def execute(self, command: UserLoginCommand) -> dict[str, str]:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            sut = UserLoginHandler(
                IAMContext(session),
                UserRepository(session),
                WebSessionRepository(session),
                Argon2PasswordHasher()
            )
            return await sut.execute(command)