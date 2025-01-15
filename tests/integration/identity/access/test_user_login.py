from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from tests.integration.identity.access.iam_test_case import IAMTestCase
                

class TestUserLoginHandler(IAMTestCase):
    async def test_user_login(self) -> None:
        # Arrange
        user = await self.create_user()

        # Act
        result = await self.execute(
            UserLoginCommand('test@mail.ru', 'protected', 'Nokia 3210'),
            Argon2PasswordHasher()
        )

        # Assert
        web_session_from_db = await self.query_web_session(
            UUID(result['session_id'])
        )
        web_session_from_db \
            .should_exist() \
            .with_user_id(result['user_id']) \
            .with_session_id(result['session_id']) \
            .with_device('Nokia 3210') \
            .with_service_life_of_up_to(result['expires_in'])

    async def execute(
        self, 
        command: UserLoginCommand, 
        password_hasher: PasswordHasher
    ) -> dict[str, str]:
        async with AsyncSession(self.engine) as session:
            await session.begin()
            handler = UserLoginHandler(
                IAMContext(session),
                password_hasher
            )
            return await handler.execute(command)