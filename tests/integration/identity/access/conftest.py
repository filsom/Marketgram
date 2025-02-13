import os
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID

from jinja2 import Environment, FileSystemLoader
import pytest
import pytest_asyncio
from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.identity.access.application.identity_service import IdentityService
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
from marketgram.identity.access.port.adapter import (
    RolesRepository,
    UsersRepository,
    WebSessionsRepository,
    user_table,
    role_table,
    web_session_table,    
)
from marketgram.identity.access.port.adapter.html_renderer import HtmlRenderer
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager


@pytest.fixture(scope='session')
def html_renderer():
    html_renderer = HtmlRenderer(
        os.getenv('EMAIL_SENDER'),
        Environment(
            loader=FileSystemLoader('templates'), 
            enable_async=True
        )
    )
    return html_renderer


@pytest_asyncio.fixture(scope='function')
async def service(engine, html_renderer):
    async with AsyncSession(engine) as session:
        return IdentityService(
            session,
            UsersRepository(session),
            RolesRepository(session),
            WebSessionsRepository(session),
            JwtTokenManager('secret'),
            AsyncMock(),
            html_renderer,
            Argon2PasswordHasher()
        )


async def delete_all(engine) -> None:
    async with AsyncSession(engine) as session:
        await session.begin()
        for table in [web_session_table, user_table, role_table]:
            await session.execute(delete(table))
        
        await session.commit()


async def query_user_with_email(engine, email: str) -> User | None:
    async with AsyncSession(engine) as session:
        await session.begin()
        return await UsersRepository(session).with_email(email)
    

async def query_user_with_id(engine, user_id: UUID) -> User | None:
    async with AsyncSession(engine) as session:
        await session.begin()
        return await UsersRepository(session).with_id(user_id)  


async def query_role(engine, user_id: UUID) -> Role:
    async with AsyncSession(engine) as session:
        await session.begin()
        return await RolesRepository(session).with_id(user_id)
    
    
async def create_user(
    engine, 
    email: str = 'test@mail.ru', 
    password: str = 'qwerty',
    is_active: bool = True
) -> User:
    async with AsyncSession(engine) as session:
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
    

async def query_web_session(engine, session_id: UUID) -> WebSession | None:
    async with AsyncSession(engine) as session:
        await session.begin()
        stmt = select(WebSession).where(WebSession.session_id == session_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    

async def create_web_session(engine, user_id: UUID) -> WebSession:
    async with AsyncSession(engine) as session:
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
    

async def query_count_web_sessions(engine, user_id: UUID) -> int:
    async with AsyncSession(engine) as session:
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