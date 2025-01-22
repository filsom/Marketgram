from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)


@dataclass
class UserAcivateCommand:
    token: str
    

class UserActivateHandler:
    def __init__(
        self,
        session: AsyncSession,
        jwt_manager: JwtTokenManager
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._users_repository = UsersRepository(session)

    async def execute(self, command: UserAcivateCommand) -> None:
        async with self._session.begin():
            user_id = self._jwt_manager.decode(
                command.token, 'user:activate'
            )
            exists_user = await self._users_repository \
                .with_id(user_id)
            
            if exists_user is None:
                raise ApplicationError()
            
            exists_user.activate()
            
            return await self._session.commit()