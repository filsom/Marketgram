from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from marketgram.identity.access.application.user_activate_command import (
    UserAcivateCommand, 
    UserActivateHandler
)
from marketgram.identity.access.application.user_login_command import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.application.user_registration_command import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.pyjwt_token_manager import (
    PyJWTTokenManager
)
from marketgram.identity.access.port.adapter.user_activate_message_maker import (
    UserActivateMessageMaker
)


class TestHandlers:
    async def test_user_activate_command(self) -> None:
        # Arrange
        user = User(
            uuid4(),
            'test@mail.ru',
            'protected',
            True
        )
        user_repository = AsyncMock()
        user_repository.with_id = AsyncMock(
            return_value=user
        )
        command = UserAcivateCommand(
            'jwt_token'
        )
        sut = UserActivateHandler(
            Mock(),
            user_repository
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.is_active == True

    async def test_user_login_command(self) -> None:
        # Arrange
        session_id = str(uuid4())
        days = 15
        created_at = datetime.now(UTC)
        expires_in = created_at + timedelta(days=days)

        user_id = uuid4()
        email = 'test@mail.ru'
        password = 'protected'

        auth_service = AsyncMock()
        auth_service.using_email = AsyncMock(
            return_value=User(
                user_id,
                email,
                password,
                True
            )
        )
        web_session_service = AsyncMock()
        web_session_service.init = AsyncMock(
            return_value=WebSession(
                user_id,
                session_id,
                created_at,
                expires_in,
                'Nokia 3210'
            ).for_browser()
        )
        command = UserLoginCommand(
            email,
            password,
            'Nokia 3210'
        )
        sut = UserLoginHandler(
            auth_service,
            web_session_service
        )

        # Act
        result = await sut.handle(command)

        # Assert
        assert {
            'session_id': str(session_id), 
            'expires_in': expires_in.strftime('%a, %d %b %Y %H:%M:%S')
        } == result

    async def test_user_registration_command(self) -> None:
        # Arrange
        user_id = uuid4()
        email = 'test@mail.ru'
        password = same_password = 'unprotected'

        user_creation_service = AsyncMock()
        user_creation_service.create = AsyncMock(
            return_value=str(user_id)
        )
        email_sender = AsyncMock()

        command = UserRegistrationCommand(
            email,
            password,
            same_password
        )
        sut = UserRegistrationHandler(
            user_creation_service,
            PyJWTTokenManager('secret'),
            UserActivateMessageMaker(),
            email_sender
        )

        # Act
        await sut.handle(command)

        # Assert
        email_sender.send_message.assert_called_once()