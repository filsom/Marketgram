from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

import pytest
from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.domain.model.web_session_factory import (
    WebSessionFactory
)
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.web_sessions_table import (
    web_session_table
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.users_table import (
    user_table
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.roles_table import (
    role_table
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.roles_repository import (
    RolesRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)
from tests.integration.identity.access.extensions import (
    UserExtensions, 
    WebSessionExtensions
)
    

class IAMTestCase:
    @pytest.fixture(autouse=True)
    def _set_async_engine(
        self, 
        engine: AsyncGenerator[AsyncEngine, None]
    ) -> None:
        self._engine = engine

    async def delete_all(self) -> None:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            for table in [web_session_table, user_table, role_table]:
                await session.execute(delete(table))
            
            await session.commit()
    
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

            stmt = (
                insert(user_table)
                .values(
                    user_id=user.user_id,
                    email=user.email,
                    password=user.password,
                    is_active=user.is_active,
                    version_id=1
                )
            )
            await session.execute(stmt)
            await session.commit()

            return user
        
    async def create_web_session(self, user_id: UUID) -> WebSession:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            web_session = WebSessionFactory().create(
                user_id, datetime.now(), 'Nokia 3210'
            )
            stmt = (
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
            await session.execute(stmt)
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
            result = await UsersRepository(session).with_email(email)
            return UserExtensions(result)
        
    async def query_user_with_id(self, user_id: UUID) -> UserExtensions:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            result = await UsersRepository(session).with_id(user_id)
            return UserExtensions(result)
                    
    async def query_role(self, user_id: UUID) -> Role:
        async with AsyncSession(self._engine) as session:
            await session.begin()
            return await RolesRepository(session).with_id(user_id)
         
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
            count = result.scalar() or 0

            return count