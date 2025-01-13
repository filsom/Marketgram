from typing import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.application.commands.user_activate import UserAcivateCommand, UserActivateHandler
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.pyjwt_token_manager import PyJWTTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import IAMContext
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import UserRepository
from marketgram.identity.access.settings import JWTManagerSecret


class TestUserActivateHandler:
    @pytest.mark.asyncio
    async def test_user_activation(self, engine: AsyncGenerator[AsyncEngine, None]) -> None:
        # Arrange
        user_id = uuid4()
        password_hasher = Argon2PasswordHasher()

        async with AsyncSession(engine) as session:
            await session.begin()
            user = User(
                user_id,
                'test@mail.ru',
                password_hasher.hash('protected')    
            )
            session.add(user)
            await session.commit()

        token_manager = PyJWTTokenManager(JWTManagerSecret('secret'))
        activation_token = token_manager.encode({
            'sub': str(user_id),
            'aud': 'user:activate'
        })
        async with AsyncSession(engine) as session:
            await session.begin()
            sut = UserActivateHandler(
                IAMContext(session),
                UserRepository(session),
                token_manager
            )

        # Act
            result = await sut.handle(UserAcivateCommand(activation_token))

        # Assert
        assert result is None

        async with AsyncSession(engine) as session:
            await session.begin()
            user = await UserRepository(session).with_id(user_id)
            
            assert user.is_active is True