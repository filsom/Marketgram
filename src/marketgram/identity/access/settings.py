import os
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader

from marketgram.identity.access.port.adapter.html_renderer import HtmlSettings


@dataclass
class EmailClientSettings:
    hostname: str
    port: int
    username: str
    password: str
    validate_certs: bool


@dataclass
class JwtHtmlSettings(HtmlSettings):
    link: str


@dataclass
class Settings:
    email_client: EmailClientSettings
    jwt_manager: str
    activate_html_settings: JwtHtmlSettings
    forgot_pwd_html_settings: JwtHtmlSettings
    jinja_env: Environment

    def for_email_client(self) -> EmailClientSettings:
        return self.email_client

    def for_jwt_manager(self):
        return self.jwt_manager
    

def identity_access_load_settings() -> Settings:
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)

    activate_html_settings = JwtHtmlSettings(
        os.environ.get('SENDER'),
        os.environ.get('SUBJECT'),
        os.environ.get('TEMPLATE_NAME'),
        os.environ.get('ACTIVATE_LINK'),
    )
    forgot_pwd_html_settings = JwtHtmlSettings(
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
    jwt_manager = os.environ.get('JWT_SECRET')
    
    return Settings(
        email_client,
        jwt_manager,
        activate_html_settings,
        forgot_pwd_html_settings,
        env
    )