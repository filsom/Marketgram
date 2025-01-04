from datetime import timedelta
import os

from dishka import Provider
from marketgram.identity.access.main.adapters_provider import AdaptersProvider
from marketgram.identity.access.main.handlers_provider import HandlersProvider
from marketgram.identity.access.main.service_provider import ServiceProvider
from marketgram.identity.access.main.settings import (
    EmailClientSettings, 
    JWTManagerSettings, 
    Settings
)


def identity_access_provider() -> tuple[Provider]:
    return (
        AdaptersProvider(),
        ServiceProvider(),
        HandlersProvider() 
    )


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