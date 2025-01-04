from typing import AsyncIterable, TypeVar

from aiosmtplib import SMTP
from argon2 import PasswordHasher
from dishka import Provider, Scope, decorate, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.common.application.message_maker import EmailMessageMaker
from marketgram.identity.access.application.commands.change_password import (
    ChangePasswordHandler
)
from marketgram.identity.access.application.commands.forgot_password import (
    ForgotPasswordHandler
)
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordHandler
)
from marketgram.identity.access.application.commands.user_activate import (
    UserActivateHandler
)
from marketgram.identity.access.application.commands.user_login import (
    UserLoginHandler
)
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.role_repository import RoleRepository
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.user_creation_service import UserCreationService
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session_repository import WebSessionRepository
from marketgram.identity.access.domain.model.web_session_service import WebSessionService
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
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    TransactionDecorator
)
from marketgram.identity.access.port.adapter.user_activate_message_maker import (
    UserActivateMessageMaker
)


Handler = TypeVar('Handler')


class Settings:
    def for_email_client(self):
        pass

    def for_jwt_manager(self):
        pass


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(
        SQLAlchemyUserRepository,
        source=UserRepository
    )
    web_session_repository = provide(
        SQLAlchemyWebSessionRepository,
        source=WebSessionRepository
    )
    role_repository = provide(
        SQLAlchemyRoleRepository,
        source=RoleRepository
    )


class EmailSenderProvider(Provider):
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

    user_activate_message_maker = provide(
        UserActivateMessageMaker, 
        scope=Scope.REQUEST, 
        provides=EmailMessageMaker,
    )

 
class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def password_hasher(self) -> PasswordSecurityHasher:
        return PasswordHasher()
    
    @provide(scope=Scope.REQUEST)
    def jwt_manager(self, settengs: Settings) -> TokenManager:
        jwt_settings = settengs.for_jwt_manager()

        return PyJWTTokenManager(jwt_settings.secret)

    services = provide_all(
        PasswordChangeService,
        UserAuthenticationService,
        UserCreationService,
        WebSessionService
    )

class HandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        ChangePasswordHandler,
        ForgotPasswordHandler,
        NewPasswordHandler,
        UserActivateHandler,
        UserLoginHandler,
        UserRegistrationHandler
    )

    @decorate
    def wrap_in_transaction(
        self, 
        handler: Handler,
        async_session: AsyncSession
    ) -> Handler:
        return TransactionDecorator(
            handler,
            async_session
        )
    

def identity_access_providers() -> tuple[Provider]:
    return (
        RepositoriesProvider(),
        EmailSenderProvider(),
        ServiceProvider(),
        HandlersProvider(),
    )