from dataclasses import dataclass

from marketgram.common.application.exceptions import ApplicationError
from marketgram.common.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.user_repository import (
    UserRepository
)


@dataclass
class UserAcivateCommand:
    token: str


class UserActivateHandler:
    def __init__(
        self,
        jwt_manager: TokenManager,
        user_repository: UserRepository
    ) -> None:
        self._jwt_manager = jwt_manager
        self._user_repository = user_repository

    async def handle(self, command: UserAcivateCommand) -> None:
        user_id = self._jwt_manager.decode(
            command.token, 'user:activate'
        )
        exists_user = await self._user_repository.with_id(user_id)
        
        if exists_user is None:
            raise ApplicationError()
        
        return exists_user.activate()