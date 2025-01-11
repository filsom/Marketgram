from unittest.mock import AsyncMock, Mock
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.commands.user_registration import UserRegistrationCommand, UserRegistrationHandler
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.pyjwt_token_manager import PyJWTTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_user_repository import SQLAlchemyUserRepository
from marketgram.identity.access.settings import JWTManagerSecret


@pytest.mark.asyncio
@pytest.mark.parametrize('email,password', [('test@mail.ru', 'unprotected')])
async def test_user_registration(
    email: str, 
    password: str,
    async_session: AsyncSession
) -> None:
    # Arrange
    user_repository = SQLAlchemyUserRepository(async_session)
    role_repository = SQLAlchemyRoleRepository(async_session)
    token_manager = PyJWTTokenManager(JWTManagerSecret('secret'))
    message_renderer = Mock()
    password_hasher = Argon2PasswordHasher(
        time_cost=2, memory_cost=19 * 1024, parallelism=1
    )
    email_sender = AsyncMock()

    sut = UserRegistrationHandler(
        user_repository,
        role_repository,
        token_manager,
        message_renderer,
        email_sender,
        password_hasher
    )

    # Act
    await sut.handle(UserRegistrationCommand(email, password))

    # Assert
    user = await user_repository.with_email('test@mail.ru')

    assert user.email == email
    assert user.password != password
    assert user.is_active == False
    sut._email_sender.send_message.assert_called_once()