from typing import AsyncGenerator

from dishka import Provider, Scope, alias, provide, provide_all
from aiosmtplib import SMTP
from jinja2 import Environment

from marketgram.common.application.email_sender import EmailSender
from marketgram.common.application.message_renderer import MessageRenderer
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)
from marketgram.identity.access.port.adapter.html_renderers import JwtTokenHtmlRenderer
from marketgram.identity.access.settings import (
    ActivateHtmlSettings, 
    ForgotPasswordHtmlSettings, 
    Settings, 
    identity_access_load_settings
)
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.common.ioc import AS
from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand,
    PasswordChangeHandler,
)
from marketgram.identity.access.application.commands.forgot_password import (
    ForgotPasswordCommand,
    ForgotPasswordHandler
)
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand,
    NewPasswordHandler
)
from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand,
    UserActivateHandler
)
from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand,
    UserLoginHandler
)
from marketgram.identity.access.application.commands.user_registration import (
    UserRegistrationHandler,
    UserRegistrationCommand,
)


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
    ) -> MessageRenderer[ActivateHtmlSettings, str]:
        return JwtTokenHtmlRenderer(
            jinja,
            settings.activate_html_settings
        )
    
    @provide
    def forgot_pwd_message_renderer(
        self, 
        settings: Settings, 
        jinja: Environment
    ) -> MessageRenderer[ForgotPasswordHtmlSettings, str]:
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
    
    # a_user_reg = alias(UserRegistrationHandler, provides=Handler[UserRegistrationCommand, None])
    # a_pwd_change = alias(PasswordChangeHandler, provides=Handler[PasswordChangeCommand, None])
    # a_new_pwd = alias(NewPasswordHandler, provides=Handler[NewPasswordCommand, None])
    # a_user_activate = alias(UserActivateHandler, provides=Handler[UserAcivateCommand, None])
    # a_user_login = alias(UserLoginHandler, provides=Handler[UserLoginCommand, dict[str, str]])
    # a_forgot_pwd = alias(ForgotPasswordHandler, provides=Handler[ForgotPasswordCommand, None])