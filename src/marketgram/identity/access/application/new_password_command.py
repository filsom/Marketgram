from dataclasses import dataclass

from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.web_session_repository import (
    WebSessionRepository
)
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)


@dataclass
class NewPasswordCommand:
    token: str
    password: str
    same_password: str


class NewPasswordHandler:
    def __init__(
        self, 
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        web_session_repository: WebSessionRepository,
        password_service: PasswordChangeService
    ) -> None:
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager
        self._web_session_repository = web_session_repository
        self._password_service = password_service
    
    async def handle(self, command: NewPasswordCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token,
            'user:password',
        )      
        user = await self._user_repository.with_id(
            user_id
        )
        self._password_service.change(
            user, 
            command.password,
            command.same_password
        )
        return await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)
        