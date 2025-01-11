from unittest.mock import AsyncMock, Mock
from uuid import uuid4
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.pyjwt_token_manager import (
    PyJWTTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_role_repository import (
    SQLAlchemyRoleRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from marketgram.identity.access.settings import ActivateHtmlSettings, JWTManagerSecret


@pytest.mark.asyncio
@pytest.mark.parametrize('email,password', [('test@mail.ru', 'unprotected')])
async def test_user_registration(
    email: str, 
    password: str,
    async_session: AsyncSession,
    activate_msg_renderer: MessageRenderer[ActivateHtmlSettings, str]
) -> None:
    # Arrange
    email_sender = AsyncMock()
    user_repository = SQLAlchemyUserRepository(async_session)
    role_repository = SQLAlchemyRoleRepository(async_session)

    sut = UserRegistrationHandler(
        user_repository,
        role_repository,
        PyJWTTokenManager(JWTManagerSecret('secret')),
        activate_msg_renderer,
        email_sender,
        Argon2PasswordHasher()
    )

    # Act
    await sut.handle(UserRegistrationCommand(email, password))

    # Assert
    user = await user_repository.with_email('test@mail.ru')

    assert user.email == email
    assert user.password != password
    assert user.is_active == False
    sut._email_sender.send_message.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize('email,password', [('test@mail.ru', 'unprotected')])
async def test_registering_for_a_busy_email(
    email: str, 
    password: str,
    async_session: AsyncSession,
    activate_msg_renderer: MessageRenderer[ActivateHtmlSettings, str]
) -> None:
    # Arrange
    email_sender = AsyncMock()
    user_repository = SQLAlchemyUserRepository(async_session)

    await user_repository.add(User(uuid4(), email, password))
    await async_session.commit()

    sut = UserRegistrationHandler(
        user_repository,
        SQLAlchemyRoleRepository(async_session),
        PyJWTTokenManager(JWTManagerSecret('secret')),
        activate_msg_renderer,
        email_sender,
        Argon2PasswordHasher()
    )

    # Act
    with pytest.raises(ApplicationError):
        await sut.handle(UserRegistrationCommand('test@mail.ru', password))