from dishka import Provider, Scope, provide, provide_all

from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.user_creation_service import (
    UserCreationService
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.web_session_service import (
    WebSessionService
)
from marketgram.identity.access.main.settings import Settings


class ServiceProvider(Provider):
    scope = Scope.REQUEST
    
    @provide
    def web_session_service(
        self,
        settings: Settings,
        web_session_repository: WebSessionRepository
    ) -> WebSessionService:
        return WebSessionService(
            settings.max_age_session,
            web_session_repository
        )

    services = provide_all(
        PasswordChangeService,
        UserAuthenticationService,
        UserCreationService,
    )