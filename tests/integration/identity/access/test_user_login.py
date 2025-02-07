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
from tests.integration.identity.access.iam_test_case import IAMTestCase
                

class TestUserLoginHandler(IAMTestCase):
    async def test_user_login(self) -> None:
        # Arrange
        await self.delete_all()
        
        await self.create_user()

        # Act
        result = await self.execute(
            UserLoginCommand('test@mail.ru', 'protected', 'Nokia 3210'),
            Argon2PasswordHasher()
        )

        # Assert
        web_session_from_db = await self.query_web_session(
            UUID(result['session_id'])
        )
        assert web_session_from_db is not None
        assert web_session_from_db.to_string_id() == result['session_id']
        assert str(web_session_from_db.user_id) == result['user_id']
        assert web_session_from_db.device == 'Nokia 3210'
        assert web_session_from_db.to_formatted_time() == result['expires_in']

    async def execute(
        self, 
        command: UserLoginCommand, 
        password_hasher: PasswordHasher
    ) -> dict[str, str]:
        async with AsyncSession(self._engine) as session:
            handler = UserLoginHandler(
                session,
                password_hasher
            )
            return await handler.execute(command)