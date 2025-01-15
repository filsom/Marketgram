from dataclasses import dataclass
from datetime import datetime

from marketgram.common.application.exceptions import ApplicationError
from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.domain.model.password_hasher import PasswordHasher
from marketgram.identity.access.domain.model.web_session_factory import (
    WebSessionFactory
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.context import (
    IAMContext
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
    UserRepository
)
from marketgram.identity.access.port.adapter.sqlalchemy_resources.web_session_repository import (
    WebSessionRepository
)


@dataclass
class UserLoginCommand:
    email: str
    password: str
    device: str
    

class UserLoginHandler:
    def __init__(
        self,
        context: IAMContext,
        password_hasher: PasswordHasher,
    ) -> None:
        self._context = context
        self._user_repository = UserRepository(context)
        self._web_session_repository = WebSessionRepository(context)
        self._password_hasher = password_hasher
        
    async def execute(self, command: UserLoginCommand) -> dict[str, str]:
        user = await self._user_repository.with_email(command.email)
        if user is None:
            raise ApplicationError()
        
        AuthenticationService(self._password_hasher) \
            .authenticate(user, command.password)
        
        await self._web_session_repository \
            .delete_this_device(user.user_id, command.device)       

        web_session = WebSessionFactory().create(
            user.user_id, datetime.now(), command.device
        )
        web_session_details = web_session.for_browser()

        await self._web_session_repository.add(web_session)
        await self._context.save_changes()

        return web_session_details