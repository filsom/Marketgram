from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
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


class NewPasswordHandler:
    def __init__(
        self, 
        user_repository: UserRepository,
        jwt_manager: TokenManager,
        web_session_repository: WebSessionRepository,
        password_hasher: PasswordSecurityHasher
    ) -> None:
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager
        self._web_session_repository = web_session_repository
        self._password_hasher = password_hasher
    
    async def handle(self, command: NewPasswordCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token, 'user:password',
        )      
        user = await self._user_repository.with_id(user_id)
        if user is None:
            raise ApplicationError()
        
        user.change_password(command.password, self._password_hasher)

        return await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)
        