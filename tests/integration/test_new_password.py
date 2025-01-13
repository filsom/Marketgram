from datetime import datetime, timedelta
from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand, 
    NewPasswordHandler
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import (
    JwtTokenManager
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.settings import JWTManagerSecret


async def test_new_password(engine: AsyncGenerator[AsyncEngine, None]) -> None:
    # Arrange
    user_id = uuid4()
    session_id = uuid4()
    new_password = 'new_protected'
    password_hasher = Argon2PasswordHasher()

    async with AsyncSession(engine) as session:
        await session.begin()
        user = User(
            user_id,
            'test@mail.ru',
            password_hasher.hash('protected')
        )
        user.activate()

        web_session = WebSession(
            user_id,
            session_id,
            datetime.now(),
            datetime.now() + timedelta(days=15),
            'Nokia 3210'
        )
        session.add_all([user, web_session])
        await session.commit()

    token_manager = JwtTokenManager(JWTManagerSecret('secret'))
    password_change_token = token_manager.encode({
        'sub': str(user_id),
        'aud': 'user:password'
    })
    async with AsyncSession(engine) as session:
        await session.begin()
        sut = NewPasswordHandler(
            IAMContext(session),
            UserRepository(session),
            WebSessionRepository(session),
            token_manager,
            password_hasher
        )

    # Act
        result = await sut.handle(
            NewPasswordCommand(password_change_token, new_password)
        )

    # Assert
    assert result is None

    async with AsyncSession(engine) as session:
        await session.begin()
        user = await UserRepository(session).with_id(user_id)
        stmt = select(WebSession).where(WebSession.user_id == user_id)
        web_sessions = (await session.execute(stmt)).scalars().all()

        assert password_hasher.verify(user.password, new_password)
        assert not web_sessions