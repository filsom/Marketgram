from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand, 
    PasswordChangeHandler
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_sessions_repository import (
    WebSessionsRepository
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestPasswordChangeHandler(IAMTestCase):
    async def test_activated_user_changes_password(self) -> None:
        # Arrange
        user = await self.create_user()
        web_session = await self.create_web_session(user.user_id)

        password_hasher = Argon2PasswordHasher()

        # Act
        await self.execute(
            PasswordChangeCommand(
                web_session.session_id, 
                'protected', 
                'new_protected'
            ),
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
        command: PasswordChangeCommand,
        password_hasher: PasswordHasher
    ) -> None:
        async with AsyncSession(self.engine) as session:
            await session.begin()
            handler = PasswordChangeHandler(
                IAMContext(session),
                UsersRepository(session),
                WebSessionsRepository(session),
                password_hasher
            )
            return await handler.execute(command)
