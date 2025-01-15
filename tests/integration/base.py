from datetime import datetime
from typing import AsyncGenerator, Self
from uuid import UUID, uuid4

import pytest
from sqlalchemy import and_, func, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.domain.model.web_session_factory import WebSessionFactory
from marketgram.identity.access.port.adapter.argon2_password_hasher import Argon2PasswordHasher
from marketgram.identity.access.port.adapter.sqlalchemy_resources.identity_table import user_table, web_session_table
from marketgram.identity.access.port.adapter.sqlalchemy_resources.role_repository import RoleRepository
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import IAMContext
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import UserRepository


class IntegrationTest:
    @pytest.fixture(autouse=True)
    def _set_async_engine(
        self, 
        engine: AsyncGenerator[AsyncEngine, None]
    ) -> None:
        self._engine = engine


class WebSessionExtensions:
    def __init__(self, web_session: WebSession | None) -> None:
        self._web_session = web_session

    def should_existing(self) -> Self:
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
    

class UserExtensions:
    def __init__(self, user: User) -> None:
        self._user = user

    @property
    def user_id(self) -> UUID:
        return self._user.user_id

    def should_exist(self) -> Self:
        assert self._user is not None
        return self

    def with_email(self, email: str) -> Self:
        assert self._user.email == email
        return self
    
    def email_is_lower(self) -> Self:
        assert self._user.email.islower()
        return self
    
    def not_activated(self) -> Self:
        assert not self._user.is_active
        return self
    
    def activated(self) -> Self:
        assert self._user.is_active
        return self
    
    def with_hashed_password(
        self, 
        password: str, 
        password_hasher: Argon2PasswordHasher
    ) -> Self:
        assert password_hasher.verify(self._user.password, password)
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
        
    async def create_web_session(self, user_id: UUID) -> WebSession:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            web_session = WebSessionFactory().create(
                user_id, datetime.now(), 'Nokia 3210'
            )
            await session.execute(
                insert(web_session_table)
                .values(
                    user_id=web_session.user_id,
                    session_id=web_session.session_id,
                    created_at=web_session.created_at,
                    expires_in=web_session.expires_in,
                    device=web_session.device,
                    version_id=1
                )
            )
            await session.commit()

            return web_session
        
    async def query_web_session(self, session_id: UUID) -> WebSessionExtensions:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            stmt = select(WebSession).where(WebSession.session_id == session_id)
            result = (await session.execute(stmt)).scalar_one_or_none()

            return WebSessionExtensions(result)
        
    async def query_user_with_email(self, email: str) -> UserExtensions:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            result = await UserRepository(IAMContext(session)).with_email(email)
            return UserExtensions(result)
        
    async def query_user_with_id(self, user_id: UUID) -> UserExtensions:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            result = await UserRepository(IAMContext(session)).with_id(user_id)
            return UserExtensions(result)
                    
    async def query_role(self, user_id: UUID) -> Role:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            return await RoleRepository(IAMContext(session)).with_id(user_id)
        
    async def query_count_web_sessions(self, user_id: UUID) -> int:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            stmt = (
                select(func.count())
                .select_from(web_session_table)
                .group_by(web_session_table.c.user_id)
                .where(web_session_table.c.user_id == user_id)
            )
            result = await session.execute(stmt)

            return result.scalar()
