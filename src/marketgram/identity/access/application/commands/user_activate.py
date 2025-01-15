from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)


@dataclass
class UserAcivateCommand:
    token: str


class UserActivateHandler:
    def __init__(
        self,
        context: IAMContext,
        jwt_manager: JwtTokenManager
    ) -> None:
        self._context = context
        self._users_repository = UsersRepository(context)
        self._jwt_manager = jwt_manager

    async def execute(self, command: UserAcivateCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token, 'user:activate'
        )
        exists_user = await self._users_repository.with_id(user_id)
        
        if exists_user is None:
            raise ApplicationError()
        
        exists_user.activate()
        
        return await self._context.save_changes()