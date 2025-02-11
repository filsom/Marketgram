from typing import AsyncGenerator

from dishka import Provider, Scope, alias, provide, provide_all
from aiosmtplib import SMTP
from jinja2 import Environment

from marketgram.common.application.email_sender import EmailSender
from marketgram.identity.access.port.adapter.html_renderer import MessageRenderer
from marketgram.identity.access.application.commands import (
    ForgotPasswordHandler,
    NewPasswordHandler,
    PasswordChangeHandler,
    UserActivateHandler,
    UserLoginHandler,
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.html_renderers import JwtTokenHtmlRenderer
from marketgram.identity.access.settings import (
    Settings, 
    identity_access_load_settings
)
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager



class IdentityAccessIoC(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return identity_access_load_settings()

    @provide(scope=Scope.APP)
    async def email_client(self, settings: Settings) -> AsyncGenerator[SMTP]:
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

    a_smtp = alias(source=SMTP, provides=EmailSender) 

    @provide
    def password_hasher(self) -> Argon2PasswordHasher:
        return Argon2PasswordHasher(
            time_cost=2,
            memory_cost=19 * 1024,
            parallelism=1
        )
    
    a_ph = alias(Argon2PasswordHasher, provides=PasswordHasher)

    @provide
    def jwt_manager(self, settings: Settings) -> JwtTokenManager:
        return JwtTokenManager(settings.jwt_manager)
    
    @provide
    def activate_jwt_message_renderer(
        self, 
        settings: Settings, 
        jinja: Environment
    ) -> MessageRenderer[str]:
        return JwtTokenHtmlRenderer(
            jinja,
            settings.activate_html_settings
        )
    
    @provide
    def forgot_pwd_message_renderer(
        self, 
        settings: Settings, 
        jinja: Environment
    ) -> MessageRenderer[str]:
        return JwtTokenHtmlRenderer(
            jinja,
            settings.forgot_pwd_html_settings
        )

    handlers = provide_all(
        UserRegistrationHandler,
        PasswordChangeHandler,
        NewPasswordHandler,
        UserActivateHandler,
        UserLoginHandler,
        ForgotPasswordHandler
    )