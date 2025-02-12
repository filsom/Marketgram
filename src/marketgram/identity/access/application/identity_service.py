from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.email_sender import (
    EmailSender,
    EMAIL_TEMPLATE,
    EMAIL_SUBJECT,
    PASSWORD_TEMPLATE,
    PASSWORD_SUBJECT
)
from marketgram.common.errors import ApplicationError
from marketgram.identity.access.application import commands as cmd
from marketgram.identity.access.domain.model.authentication_service import AuthenticationService
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.identity.access.domain.model.web_session_factory import WebSessionFactory
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.html_renderer import HtmlRenderer
from marketgram.identity.access.port.adapter import (
    UsersRepository,
    RolesRepository,
    WebSessionsRepository
)


class IdentityService:
    def __init__(
        self,
        session: AsyncSession,
        users_repository: UsersRepository,
        roles_repository: RolesRepository,
        web_sessions_repository: WebSessionsRepository,
        jwt_manager: JwtTokenManager,
        email_sender: EmailSender,
        html_renderer: HtmlRenderer,
        password_hasher: PasswordHasher
    ) -> None:
        self.session = session
        self.users_repository = users_repository
        self.roles_repository = roles_repository
        self.web_sessions_repository = web_sessions_repository
        self.jwt_manager = jwt_manager
        self.email_sender = email_sender
        self.html_renderer = html_renderer
        self.password_hasher = password_hasher

    async def create_user(self, command: cmd.UserCreationCommand) -> None:
        async with self.session.begin():
            user = await self.users_repository.with_email(command.email)
            if user is not None:
                raise ApplicationError()
            
            new_user = UserFactory(self.password_hasher) \
                .create(command.email, command.password)
            role = Role(new_user.user_id, Permission.USER)

            self.users_repository.add(new_user)
            self.roles_repository.add(role)
            
            jwt_token = self.jwt_manager.encode(
                datetime.now(UTC),
                {'sub': new_user.to_string_id(), 'aud': 'user:activate'}
            )
            message = await self.html_renderer.render(
                EMAIL_TEMPLATE,
                EMAIL_SUBJECT,
                new_user.email, 
                {'token': jwt_token}
            )
            await self.email_sender.send_message(message)
            await self.session.commit()

    async def authenticate_user(self, command: cmd.AuthenticateUserCommand) -> dict[str, str]:
        async with self.session.begin():
            user = await self.users_repository.with_email(command.email)
            if user is None:
                raise ApplicationError()
            
            AuthenticationService(self.password_hasher) \
                .authenticate(user, command.password)
            
            await self.web_sessions_repository \
                .delete_this_device(user.user_id, command.device)       

            web_session = WebSessionFactory().create(
                user.user_id, datetime.now(), command.device
            )
            web_session_details = web_session.for_browser()
            self.web_sessions_repository.add(web_session)
            await self.session.commit()
            return web_session_details
        
    async def activate_user(self, token: str) -> None:
        async with self.session.begin():
            user_id = self.jwt_manager.decode(token, 'user:activate')
            exists_user = await self.users_repository.with_id(user_id)
            
            if exists_user is None:
                raise ApplicationError()
            
            exists_user.activate()
            await self.session.commit()

    async def change_user_password(self, command: cmd.ChangePasswordCommand) -> None:
        async with self.session.begin():
            web_session = await self.web_sessions_repository \
                .lively_with_id(command.session_id, datetime.now())
            
            if web_session is None:
                raise ApplicationError()
            
            user = await self.users_repository.with_id(web_session.user_id)

            AuthenticationService(self.password_hasher) \
                .authenticate(user, command.old_password)

            user.change_password(command.new_password, self.password_hasher)

            await self.web_sessions_repository \
                .delete_all_with_user_id(user.user_id)
            await self.session.commit()

    async def set_new_password(self, command: cmd.SetNewPasswordCommand) -> None:
        async with self.session.begin():
            user_id = self.jwt_manager.decode(command.token, 'user:password')      
            user = await self.users_repository.with_id(user_id)
            if user is None:
                raise ApplicationError()
            
            user.change_password(command.password, self.password_hasher)

            await self.web_sessions_repository \
                .delete_all_with_user_id(user.user_id)
            await self.session.commit()

    async def user_forgot_password(self, email: str) -> None:
        async with self.session.begin():
            user = await self.users_repository.with_email(email) 
            if user is None or not user.is_active:
                return 
            
            jwt_token = self.jwt_manager.encode(
                datetime.now(UTC), {'sub': user.to_string_id(), 'aud': 'user:password'}
            )
            message = await self.html_renderer.render(
                PASSWORD_TEMPLATE,
                PASSWORD_SUBJECT,
                user.email, 
                {'token': jwt_token}
            )
            await self.email_sender.send_message(message)
            await self.session.commit()