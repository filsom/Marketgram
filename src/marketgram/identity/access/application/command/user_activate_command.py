from dataclasses import dataclass

from marketgram.identity.access.application.jwt_manager import TokenManager
from marketgram.identity.access.domain.model.identity.user_repository import (
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
            command.token,
            'user:activate'
        )
        exists_user = await self._user_repository \
            .with_id(user_id)
        
        return exists_user.activate()