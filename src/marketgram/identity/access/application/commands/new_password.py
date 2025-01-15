from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)


@dataclass
class NewPasswordCommand:
    token: str
    password: str


class NewPasswordHandler:
    def __init__(
        self, 
        context: IAMContext,
        jwt_manager: JwtTokenManager,
        password_hasher: PasswordHasher
    ) -> None:
        self._context = context
        self._user_repository = UserRepository(context)
        self._web_session_repository = WebSessionRepository(context)
        self._jwt_manager = jwt_manager
        self._password_hasher = password_hasher
    
    async def execute(self, command: NewPasswordCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token, 'user:password',
        )      
        user = await self._user_repository.with_id(user_id)
        if user is None:
            raise ApplicationError()
        
        user.change_password(command.password, self._password_hasher)

        await self._web_session_repository \
            .delete_all_with_user_id(user.user_id)
        
        return await self._context.save_changes()
        