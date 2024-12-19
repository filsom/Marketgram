from dataclasses import dataclass

from marketgram.identity.access.application.id_provider import IdProvider
from marketgram.identity.access.domain.model.access.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.identity.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.domain.model.identity.user_repository import (
    UserRepository
)


@dataclass
class ChangePasswordCommand:
    old_password: str
    new_password: str


class ChangePasswordHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        id_provider: IdProvider,
        web_session_repository: WebSessionRepository,
    ) -> None:
        self._user_repository = user_repository
        self._id_provider = id_provider
        self._web_session_repository = web_session_repository

    async def handle(self, command: ChangePasswordCommand) -> None:
        exists_user = await self._user_repository \
            .with_id(self._id_provider.provided_id())
        
        AuthenticationService().authenticate(
            exists_user,
            command.old_password
        )
        exists_user.change_password(command.new_password)
        
        return await (
            self._web_session_repository
            .delete_all_with_user_id(exists_user.user_id)
        )