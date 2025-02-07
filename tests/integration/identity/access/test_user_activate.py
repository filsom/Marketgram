from datetime import UTC, datetime
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand, 
    UserActivateHandler
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestUserActivateHandler(IAMTestCase):
    async def test_user_activation(self) -> None:
        # Arrange
        await self.delete_all()
        
        user = await self.create_user(is_active=False)
        
        token_manager = JwtTokenManager('secret')
        activation_token = token_manager.encode(
            datetime.now(UTC),
            {'sub': user.to_string_id(), 'aud': 'user:activate'}
        )

        # Act
        await self.execute(
            UserAcivateCommand(activation_token),
            token_manager
        )

        # Assert
        user_from_db = await self.query_user_with_id(user.user_id)

        assert user_from_db is not None
        assert user_from_db.is_active

    async def execute(
        self, 
        command: UserAcivateCommand,
        token_manager: JwtTokenManager
    ) -> None:
        async with AsyncSession(self._engine) as session:
            handler = UserActivateHandler(
                session,
                token_manager
            )
            return await handler.execute(command)