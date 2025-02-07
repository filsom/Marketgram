from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand, 
    PasswordChangeHandler
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestPasswordChangeHandler(IAMTestCase):
    async def test_activated_user_changes_password(self) -> None:
        # Arrange
        await self.delete_all()
        
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
        
        assert user_from_db is not None
        assert password_hasher.verify(user_from_db.password, 'new_protected')

        count_web_sessions = await self.query_count_web_sessions(user_from_db.user_id)
        assert count_web_sessions == 0

    async def execute(
        self,
        command: PasswordChangeCommand,
        password_hasher: PasswordHasher
    ) -> None:
        async with AsyncSession(self._engine) as session:
            handler = PasswordChangeHandler(
                session,
                password_hasher
            )
            return await handler.execute(command)
