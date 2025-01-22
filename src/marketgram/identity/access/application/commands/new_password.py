from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.password_hasher import (
    PasswordHasher
)
from marketgram.identity.access.port.adapter.jwt_token_manager import JwtTokenManager
from marketgram.identity.access.port.adapter.sqlalchemy_resources.users_repository import (
    UsersRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_sessions_repository import (
    WebSessionsRepository
)


@dataclass
class NewPasswordCommand:
    token: str
    password: str


class NewPasswordHandler:
    def __init__(
        self, 
        session: AsyncSession,
        jwt_manager: JwtTokenManager,
        password_hasher: PasswordHasher
    ) -> None:
        self._session = session
        self._jwt_manager = jwt_manager
        self._password_hasher = password_hasher
        self._users_repository = UsersRepository(session)
        self._web_sessions_repository = WebSessionsRepository(session)
    
    async def execute(self, command: NewPasswordCommand) -> None:
        async with self._session.begin():
            user_id = self._jwt_manager.decode(
                command.token, 'user:password',
            )      
            user = await self._users_repository.with_id(user_id)
            if user is None:
                raise ApplicationError()
            
            user.change_password(command.password, self._password_hasher)

            await self._web_sessions_repository \
                .delete_all_with_user_id(user.user_id)
            
            return await self._session.commit()
        