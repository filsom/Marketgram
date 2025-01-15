from datetime import datetime, timedelta
from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand, 
    PasswordChangeHandler
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
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


async def test_change_user_password(engine: AsyncGenerator[AsyncEngine, None]) -> None:
    # Arrange
    user_id = uuid4()
    session_id = uuid4()
    old_password = 'old_protected'
    new_password = 'new_unprotected'
    
    password_hasher = Argon2PasswordHasher()

    async with AsyncSession(engine) as session:
        await session.begin()
        user = User(
            user_id,
            'test@mail.ru',
            password_hasher.hash(old_password)
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

    async with AsyncSession(engine) as session:
        await session.begin()
        sut = PasswordChangeHandler(
            IAMContext(session),
            UserRepository(session),
            WebSessionRepository(session),
            password_hasher
        )

    # Act
        await sut.handle(PasswordChangeCommand(session_id, old_password, new_password))

    # Assert
    async with AsyncSession(engine) as session:
        await session.begin()
        user = await UserRepository(session).with_id(user_id)
        stmt = select(WebSession).where(WebSession.user_id == user_id)
        web_sessions = (await session.execute(stmt)).scalars().all()

        assert password_hasher.verify(user.password, new_password)
        assert not web_sessions


