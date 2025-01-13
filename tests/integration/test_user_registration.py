from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

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


@pytest.mark.asyncio
async def test_user_registration(
    engine: AsyncGenerator[AsyncEngine, None],
    activate_msg_renderer: MessageRenderer[ActivateHtmlSettings, str]
) -> None:
    # Arrange
    email = 'test@mail.ru'
    password = 'unprotected'

    password_hasher = Argon2PasswordHasher()
    email_sender = AsyncMock()

    async with AsyncSession(engine) as session:
        await session.begin()
        sut = UserRegistrationHandler(
            IAMContext(session),
            UserRepository(session),
            RoleRepository(session),
            JwtTokenManager(JWTManagerSecret('secret')),
            Mock(),
            email_sender,
            password_hasher
        )

    # Act
        await sut.handle(UserRegistrationCommand(email, password))

    # Assert
    sut._email_sender.send_message.assert_called_once()

    async with AsyncSession(engine) as session:
        await session.begin()
        user = await UserRepository(session).with_email(email)
        role = await RoleRepository(session).with_id(user.user_id)

        assert user.email.islower()
        assert user.email == email
        assert password_hasher.verify(user.password, password)
        assert user.is_active == False
        assert role.permission == Permission.USER