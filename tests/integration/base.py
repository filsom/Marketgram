from datetime import datetime
from typing import AsyncGenerator, Self
from uuid import UUID, uuid4

import pytest
from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.domain.model.web_session_factory import WebSessionFactory
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.sqlalchemy_resources.identity_table import user_table


class IntegrationTest:
    @pytest.fixture(autouse=True)
    def _set_async_engine(
        self, 
        engine: AsyncGenerator[AsyncEngine, None]
    ) -> None:
        self._engine = engine


class WebSessionExpression:
    def __init__(self, web_session: WebSession | None) -> None:
        self._web_session = web_session

    def should_exsiting(self) -> Self:
        assert self._web_session is not None
        return self
    
    def with_session_id(self, session_id: str) -> Self:
        assert self._web_session.to_string_id() == session_id
        return self

    def with_user_id(self, user_id: str) -> Self:
        assert self._web_session.user_id == user_id
        return self
    
    def with_device(self, device: str) -> Self:
        assert self._web_session.device == device
        return self

    def with_service_life_of_up_to(self, expires_in: str) -> Self:
        assert self._web_session.to_formatted_time() == expires_in
        return self

    

class IAMTestCase(IntegrationTest):
    async def create_user(
        self, 
        email: str = 'test@mail.ru', 
        password: str = 'protected',
        is_active: bool = True
    ) -> User:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            user = UserFactory(Argon2PasswordHasher()).create(
                email, password
            )
            if is_active:
                user.activate()

            await session.execute(
                insert(user_table)
                .values(
                    user_id=user.user_id,
                    email=user.email,
                    password=user.password,
                    is_active=user.is_active,
                    version_id=1
                )
            )
            await session.commit()

            return user
        
    async def query_web_session(self, session_id: UUID) -> WebSessionExpression:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            stmt = select(WebSession).where(
                WebSession.session_id == session_id,
            )
            result = (await session.execute(stmt)).scalar_one_or_none()

            return WebSessionExpression(result)

    async def create_web_session(self, user_id: UUID) -> WebSession:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            web_session = WebSessionFactory().create(
                user_id, datetime.now(), 'Nokia 3210'
            )
            session.add(web_session)
            await session.commit()

            return web_session
