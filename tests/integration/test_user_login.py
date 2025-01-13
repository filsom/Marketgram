from typing import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
    UserLoginHandler
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
from tests.integration.conftest import IntegrationTest
                

class TestUserLoginHandler(IntegrationTest):
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'email,password,device', [('test@mail.ru', 'protected', 'Nokia 3210')]
    )
    async def test_user_login(
        self,
        email: str, 
        password: str,
        device: str, 
        engine: AsyncGenerator[AsyncEngine]
    ) -> None:
        # Arrange
        user_id = uuid4()
        password_hasher = Argon2PasswordHasher()

        async with AsyncSession(engine) as session:
            await session.begin()
            user = User(
                user_id,
                email,
                password_hasher.hash(password)    
            )
            user.activate()

            session.add(user)
            await session.commit()

        async with AsyncSession(engine) as session:
            await session.begin()
            sut = UserLoginHandler(
                IAMContext(session),
                UserRepository(session),
                WebSessionRepository(session),
                password_hasher
            )

        # Act
            result = await sut.handle(UserLoginCommand(email, password, device))

        # Assert
        async with AsyncSession(engine) as session:
            await session.begin()
            stmt = select(WebSession).where(WebSession.user_id == user_id)
            web_session = (await session.execute(stmt)).scalar()

            assert result['session_id'] == web_session.to_string_id()
            assert result['expires_in'] == web_session.to_formatted_time()
            assert result['user_id'] == str(user_id)
            assert web_session.device == device