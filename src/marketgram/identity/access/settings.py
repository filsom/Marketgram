import os
from dataclasses import dataclass

from marketgram.common.application.message_renderer import JwtHtmlSettings


@dataclass
class EmailClientSettings:
    hostname: str
    port: int
    username: str
    password: str
    validate_certs: bool


@dataclass
class JWTManagerSettings:
    secret: str


class ActivateHtmlSettings(JwtHtmlSettings):
    pass


class ForgotPasswordHtmlSettings(JwtHtmlSettings):
    pass


@dataclass
class Settings:
    email_client: EmailClientSettings
    jwt_manager: JWTManagerSettings
    activate_html_settings: ActivateHtmlSettings
    forgot_pwd_html_settings: ForgotPasswordHtmlSettings

    def for_email_client(self) -> EmailClientSettings:
        return self.email_client

    def for_jwt_manager(self):
        return self.jwt_manager
    

def identity_access_load_settings() -> Settings:
    activate_html_settings = ActivateHtmlSettings(
        os.environ.get('SENDER'),
        os.environ.get('SUBJECT'),
        os.environ.get('TEMPLATE_NAME'),
        os.environ.get('ACTIVATE_LINK'),
    )
    forgot_pwd_html_settings = ActivateHtmlSettings(
        os.environ.get('SENDER'),
        os.environ.get('SUBJECT'),
        os.environ.get('TEMPLATE_NAME'),
        os.environ.get('FORGOT_PWD_LINK'),
    )
    email_client = EmailClientSettings(
        os.environ.get('HOSTNAME'),
        os.environ.get('PORT'),
        os.environ.get('USERNAME'),
        os.environ.get('PASSWORD'),
        os.environ.get('VALIDATE_CERTS')
    )
    jwt_manager = JWTManagerSettings(
        os.environ.get('JWT_SECRET')
    )
    return Settings(
        email_client,
        jwt_manager,
        activate_html_settings,
        forgot_pwd_html_settings
    )