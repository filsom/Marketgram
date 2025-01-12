from uuid import uuid4
import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'email,password,device', [('test@mail.ru', 'protected', 'Nokia 3210')]
)
async def test_user_login(
    email: str, 
    password: str,
    device: str, 
    async_session: AsyncSession
) -> None:
    # Arrange
    user_repository = UserRepository(async_session)
    password_hasher = Argon2PasswordHasher()

    user_id = uuid4()
    user = User(
        user_id,
        email,
        password_hasher.hash(password)    
    )
    user.activate()

    await user_repository.add(user)
    await async_session.commit()

    sut = UserLoginHandler(
        user_repository,
        password_hasher,
        WebSessionRepository(async_session)
    )

    # Act
    result = await sut.handle(UserLoginCommand(
        email, password, device
    ))

    # Assert
    stmt = select(WebSession).where(WebSession.user_id == user_id)
    web_session = (await async_session.execute(stmt)).scalar()

    assert result['session_id'] == web_session.to_string_id()
    assert result['expires_in'] == web_session.to_formatted_time()
    assert result['user_id'] == str(user_id)
    assert web_session.device == device