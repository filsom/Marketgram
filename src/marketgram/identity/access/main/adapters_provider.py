from typing import AsyncIterable
from aiosmtplib import SMTP
from argon2 import PasswordHasher
from dishka import Provider, Scope, provide

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
from marketgram.identity.access.main.settings import Settings, identity_access_load_settings
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


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repository(self, async_session: AS) -> UserRepository:
        return SQLAlchemyUserRepository(async_session)
    
    @provide
    def web_session_repository(self, async_session: AS) -> WebSessionRepository:
        return SQLAlchemyWebSessionRepository(async_session)
    
    @provide
    def role_repository(self, async_session: AS) -> RoleRepository:
        return SQLAlchemyRoleRepository(async_session)
    
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
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
    def jwt_manager(self, settengs: Settings) -> TokenManager:
        jwt_settings = settengs.for_jwt_manager()

        return PyJWTTokenManager(jwt_settings.secret)
    
    @provide
    def password_hasher(self) -> PasswordSecurityHasher:
        return PasswordHasher()
    
    user_activate_message_maker = provide(
        UserActivateMessageMaker, 
        scope=Scope.REQUEST, 
        provides=EmailMessageMaker,
    )