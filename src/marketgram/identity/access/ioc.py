from typing import AsyncIterable

from dishka import Provider, Scope, decorate, provide, provide_all
from aiosmtplib import SMTP
from argon2 import PasswordHasher

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.common.application.message_maker import EmailMessageMaker
from marketgram.common.ioc import AS
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.role_repository import RoleRepository
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session_repository import WebSessionRepository
from marketgram.identity.access.settings import Settings, identity_access_load_settings
from marketgram.identity.access.port.adapter.pyjwt_token_manager import PyJWTTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_role_repository import (
    SQLAlchemyRoleRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_web_session_repository import (
    SQLAlchemyWebSessionRepository
)
from marketgram.identity.access.port.adapter.user_activate_message_maker import (
    UserActivateMessageMaker
)
from marketgram.common.ioc import AS
from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand,
    PasswordChange,
)
from marketgram.identity.access.application.commands.forgot_password import (
    ForgottenPasswordCommand,
    ForgottenPassword,
    Handler,
    Cmd
)
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand,
    NewPassword
)
from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand,
    UserActivate
)
from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand,
    UserLoginHandler
)
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistration,
    UserRegistrationCommand,
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    TransactionDecorator
)
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.user_creation_service import (
    UserCreationService
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.web_session_service import (
    WebSessionService
)


class IdentityAccessIoC(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def identity_access_settings(self) -> Settings:
        return identity_access_load_settings()

    @provide(scope=Scope.APP)
    async def provider_email_client(
        self,
        settings: Settings
    ) -> AsyncIterable[EmailSender]:
        email_settings = settings.for_email_client()

        client = SMTP(
            hostname=email_settings.hostname, 
            port=email_settings.port,
            username=email_settings.username,
            password=email_settings.password,
            validate_certs=email_settings.validate_certs
        )
        async with client:
            yield client   

    @provide
    def user_repository(self, async_session: AS) -> UserRepository:
        return SQLAlchemyUserRepository(async_session)
    
    @provide
    def web_session_repository(self, async_session: AS) -> WebSessionRepository:
        return SQLAlchemyWebSessionRepository(async_session)
    
    @provide
    def role_repository(self, async_session: AS) -> RoleRepository:
        return SQLAlchemyRoleRepository(async_session)

    dependencies = provide_all(
        PasswordChangeService,
        UserAuthenticationService,
        UserCreationService,
        provide(
            UserActivateMessageMaker, 
            provides=EmailMessageMaker
        ),
        provide(
            lambda hasher: PasswordHasher(),
            provides=PasswordSecurityHasher
        )
    )

    @provide
    def jwt_manager(self, settings: Settings) -> TokenManager:
        return PyJWTTokenManager(settings.for_jwt_manager())

    @provide
    def web_session_service(
        self,
        settings: Settings,
        web_session_repository: WebSessionRepository
    ) -> WebSessionService:
        return WebSessionService(
            settings.max_age_session,
            web_session_repository
        )

    handlers = provide_all(
        provide(
            PasswordChange, 
            provides=Handler[PasswordChangeCommand, None]
        ),
        provide(
            ForgottenPassword, 
            provides=Handler[ForgottenPasswordCommand, None]
        ),
        provide(
            NewPassword, 
            provides=Handler[NewPasswordCommand, None]
        ),
        provide(
            UserActivate, 
            provides=Handler[UserAcivateCommand, None]
        ),
        provide(
            UserLoginHandler, 
            provides=Handler[UserLoginCommand, dict[str, str]]
        ),
        provide(
            UserRegistration, 
            provides=Handler[UserRegistrationCommand, None]
        )
    )

    @decorate
    def wrapped_handler(
        self, 
        handler: Handler[Cmd], 
        async_session: AS
    ) -> Handler[Cmd]:
        return TransactionDecorator(
            handler,
            async_session
        )