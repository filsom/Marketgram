import os
from datetime import timedelta
from dataclasses import dataclass


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


@dataclass
class Settings:
    email_client: EmailClientSettings
    jwt_manager: JWTManagerSettings
    max_age_session: timedelta

    def for_email_client(self) -> EmailClientSettings:
        return self.email_client

    def for_jwt_manager(self):
        return self.jwt_manager
    

def identity_access_load_settings() -> Settings:
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
        timedelta(days=15)
    )