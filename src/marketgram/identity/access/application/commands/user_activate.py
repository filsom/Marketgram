from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.transaction_decorator import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)


@dataclass
class UserAcivateCommand:
    token: str


class UserActivateHandler:
    def __init__(
        self,
        context: IAMContext,
        user_repository: UserRepository,
        jwt_manager: JwtTokenManager
    ) -> None:
        self._context = context
        self._user_repository = user_repository
        self._jwt_manager = jwt_manager

    async def handle(self, command: UserAcivateCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token, 'user:activate'
        )
        exists_user = await self._user_repository.with_id(user_id)
        
        if exists_user is None:
            raise ApplicationError()
        
        exists_user.activate()
        
        return await self._context.save_changes()