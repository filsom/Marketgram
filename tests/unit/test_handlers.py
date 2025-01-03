from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from marketgram.identity.access.application.user_registration_command import UserRegistrationCommand, UserRegistrationHandler
from marketgram.identity.access.port.adapter.pyjwt_token_manager import PyJWTTokenManager
from marketgram.identity.access.port.adapter.user_activate_message_maker import UserActivateMessageMaker


class TestHandlers:
    async def test_user_registration_command(self) -> None:
        # Arrange
        user_id = uuid4()
        email = 'test@mail.ru'
        password = same_password = 'unprotected'

        user_creation_service = AsyncMock()
        user_creation_service.create = AsyncMock(
            return_value=str(user_id)
        )
        jwt_manager = PyJWTTokenManager('secret')
        jwt_token = jwt_manager.encode({
            'sub': str(user_id),
            'aud': 'user:activate'
        })
        message_maker = UserActivateMessageMaker()
        message = message_maker.make(jwt_token, email)

        email_sender = AsyncMock()
        await email_sender('send_message', message=message)

        command = UserRegistrationCommand(
            email,
            password,
            same_password
        )
        sut = UserRegistrationHandler(
            user_creation_service,
            jwt_manager,
            message_maker,
            email_sender
        )

        # Act
        await sut.handle(command)

        # Assert
        email_sender.assert_called_once_with(
            'send_message',
            message=message
        )

        