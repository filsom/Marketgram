from dishka import Provider

from marketgram.identity.access.main.adapters_provider import AdaptersProvider
from marketgram.identity.access.main.handlers_provider import HandlersProvider
from marketgram.identity.access.main.service_provider import ServiceProvider


def identity_access_provider() -> tuple[Provider]:
    return (
        AdaptersProvider(),
        ServiceProvider(),
        HandlersProvider() 
    )