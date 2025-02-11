import os
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader


@dataclass
class EmailClientSettings:
    hostname: str
    port: int
    username: str
    password: str
    validate_certs: bool


@dataclass
class Settings:
    email_client: EmailClientSettings
    jwt_manager: str
    jinja_env: Environment

    def for_email_client(self) -> EmailClientSettings:
        return self.email_client

    def for_jwt_manager(self):
        return self.jwt_manager
    

def identity_access_load_settings() -> Settings:
    loader = FileSystemLoader('templates')
    environment = Environment(loader=loader)

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
        environment
    )