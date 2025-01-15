from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand, 
    NewPasswordHandler
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestNewPasswordHandler(IAMTestCase):
    async def test_new_password(self) -> None:
        # Arrange        
        user = await self.create_user()
        await self.create_web_session(user.user_id)

        password_hasher = Argon2PasswordHasher()
        token_manager = JwtTokenManager('secret')
        password_change_token = token_manager.encode({
            'sub': user.to_string_id(),
            'aud': 'user:password'
        })

        # Act
        await self.execute(
            NewPasswordCommand(password_change_token, 'new_protected'),
            token_manager,
            password_hasher
        )

        # Assert
        user_from_db = await self.query_user_with_id(user.user_id)
        user_from_db \
            .should_exist() \
            .with_hashed_password('new_protected', password_hasher)

        count_web_sessions = await self.query_count_web_sessions(user_from_db.user_id)
        assert not count_web_sessions

    async def execute(
        self,
        command: NewPasswordCommand,
        token_manager: JwtTokenManager,
        password_hasher: PasswordHasher
    ) -> None:
        async with AsyncSession(self.engine) as session:
            await session.begin()
            handler = NewPasswordHandler(
                IAMContext(session),
                token_manager,
                password_hasher
            )
            return await handler.execute(command)