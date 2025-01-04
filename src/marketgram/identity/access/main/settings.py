import os
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

    def for_email_client(self) -> EmailClientSettings:
        return self.email_client

    def for_jwt_manager(self):
        return self.jwt_manager
    

def identity_access_load_settings() -> Settings:
    email_client = EmailClientSettings(
        os.environ('HOSTNAME'),
        os.environ('PORT'),
        os.environ('USERNAME'),
        os.environ('PASSWORD'),
        os.environ('VALIDATE_CERTS')
    )
    jwt_manager = JWTManagerSettings(
        os.environ('JWT_SECRET')
    )
    return Settings(
        email_client,
        jwt_manager
    )