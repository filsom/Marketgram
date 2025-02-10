from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.authentication_service import AuthenticationService
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.domain.model.web_session_factory import WebSessionFactory
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.roles_repository import (
    RolesRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_sessions_repository import (
    WebSessionsRepository
)


@dataclass
class UserRegistrationCommand:
    email: str
    password: str
    

class UserRegistrationHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._roles_repository = RolesRepository(session)
        
    async def execute(self, command: UserRegistrationCommand) -> None:
        async with self._session.begin():
            user = await self._users_repository.with_email(command.email)
            if user is not None:
                raise ApplicationError()
            
            new_user = UserFactory(self._password_hasher) \
                .create(command.email, command.password)
            role = Role(new_user.user_id, Permission.USER)

            self._users_repository.add(new_user)
            self._roles_repository.add(role)
            
            jwt_token = self._jwt_manager.encode(
                datetime.now(UTC),
                {'sub': new_user.to_string_id(), 'aud': 'user:activate'}
            )
            message = self._message_renderer.render(command.email, jwt_token)
            await self._email_sender.send_message(message)

            await self._session.commit()


@dataclass
class UserLoginCommand:
    email: str
    password: str
    device: str
    

class UserLoginHandler:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher,
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._web_sessions_repository = WebSessionsRepository(session)
        
    async def execute(self, command: UserLoginCommand) -> dict[str, str]:
        async with self._session.begin():
            user = await self._users_repository.with_email(command.email)
            if user is None:
                raise ApplicationError()
            
            AuthenticationService(self._password_hasher) \
                .authenticate(user, command.password)
            
            await self._web_sessions_repository \
                .delete_this_device(user.user_id, command.device)       

            web_session = WebSessionFactory().create(
                user.user_id, datetime.now(), command.device
            )
            web_session_details = web_session.for_browser()

            await self._web_sessions_repository.add(web_session)
            await self._session.commit()

            return web_session_details
        

@dataclass
class UserAcivateCommand:
    token: str
    

class UserActivateHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._users_repository = UsersRepository(session)

    async def execute(self, command: UserAcivateCommand) -> None:
        async with self._session.begin():
            user_id = self._jwt_manager.decode(
                command.token, 'user:activate'
            )
            exists_user = await self._users_repository \
                .with_id(user_id)
            
            if exists_user is None:
                raise ApplicationError()
            
            exists_user.activate()
            
            await self._session.commit()


@dataclass
class PasswordChangeCommand:
    session_id: UUID
    old_password: str
    new_password: str


class PasswordChangeHandler:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._web_sessions_repository = WebSessionsRepository(session)

    async def execute(self, command: PasswordChangeCommand) -> None:
        async with self._session.begin():
            web_session = await self._web_sessions_repository \
                .lively_with_id(command.session_id, datetime.now())
            
            if web_session is None:
                raise ApplicationError()
            
            user = await self._users_repository.with_id(web_session.user_id)

            AuthenticationService(self._password_hasher) \
                .authenticate(user, command.old_password)

            user.change_password(command.new_password, self._password_hasher)

            await self._web_sessions_repository \
                .delete_all_with_user_id(user.user_id)
            await self._session.commit()


@dataclass
class NewPasswordCommand:
    token: str
    password: str


class NewPasswordHandler:
    def __init__(
        self, 
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._web_sessions_repository = WebSessionsRepository(session)
    
    async def execute(self, command: NewPasswordCommand) -> None:
        async with self._session.begin():
            user_id = self._jwt_manager.decode(
                command.token, 'user:password',
            )      
            user = await self._users_repository.with_id(user_id)
            if user is None:
                raise ApplicationError()
            
            user.change_password(command.password, self._password_hasher)

            await self._web_sessions_repository \
                .delete_all_with_user_id(user.user_id)
            await self._session.commit()


@dataclass
class ForgotPasswordCommand:
    email: str


class ForgotPasswordHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        message_renderer: MessageRenderer[str],
        email_sender: EmailSender
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._message_renderer = message_renderer
        self._email_sender = email_sender
        self._users_repository = UsersRepository(session)
    
    async def execute(self, command: ForgotPasswordCommand) -> None:
        async with self._session.begin():
            user = await self._users_repository.with_email(command.email) 
            if user is None or not user.is_active:
                return 
            
            jwt_token = self._jwt_manager.encode(
                datetime.now(UTC),
                {'sub': user.to_string_id(), 'aud': 'user:password'}
            )
            message = self._message_renderer.render(user.email, jwt_token)
            await self._email_sender.send_message(message)
            
            await self._session.commit()