from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand, 
    UserActivateHandler
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)
from tests.integration.identity.access.iam_test_case import IAMTestCase


class TestUserActivateHandler(IAMTestCase):
    async def test_user_activation(self) -> None:
        # Arrange
        user = await self.create_user()

        token_manager = JwtTokenManager('secret')
        activation_token = token_manager.encode({
            'sub': user.to_string_id(),
            'aud': 'user:activate'
        })

        # Act
        await self.execute(
            UserAcivateCommand(activation_token),
            token_manager
        )

        # Assert
        user_from_db = await self.query_user_with_id(user.user_id)
        user_from_db \
            .should_exist() \
            .activated()

    async def execute(
        self, 
        command: UserAcivateCommand,
        token_manager: JwtTokenManager
    ) -> None:
        async with AsyncSession(self.engine) as session:
            await session.begin()
            handler = UserActivateHandler(
                IAMContext(session),
                token_manager
            )
            return await handler.execute(command)