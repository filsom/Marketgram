from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from marketgram.identity.access.application.change_password_command import (
    ChangePasswordCommand, 
    ChangePasswordHandler
)
from marketgram.identity.access.application.forgot_password_coomand import (
    ForgotPasswordCommand, 
    ForgotPasswordHandler
)
from marketgram.identity.access.application.new_password_command import (
    NewPasswordCommand, 
    NewPasswordHandler
)
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
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_repository import UserRepository
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.pyjwt_token_manager import (
    PyJWTTokenManager
)
from marketgram.identity.access.port.adapter.user_activate_message_maker import (
    UserActivateMessageMaker
)


class TestHandlers:
    async def test_change_password_command(self) -> None:
        # Arrange
        new_password = same_password ='new_unprotected'
        new_protected_password = 'new_protected'
        user = User(
            uuid4(),
            'test@mail.ru',
            'protected',
            True
        )
        id_provider = Mock()
        auth_service = AsyncMock()
        auth_service.using_id = AsyncMock(
            return_value=user
        )
        password_service = self.mock_password_service(
            new_protected_password
        )
        web_session_repository = AsyncMock()

        command = ChangePasswordCommand(
            user.password,
            new_password,
            same_password
        )
        sut = ChangePasswordHandler(
            id_provider,
            auth_service,
            password_service,
            web_session_repository
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.password == new_protected_password
        web_session_repository \
            .delete_all_with_user_id \
            .assert_called_once_with(user.user_id)

    async def test_forgot_password_command(self) -> None:
        # Arrange
        email = 'test@mail.ru'
        user = User(
            uuid4(),
            email,
            'protected',
            True
        )
        user_repository = self.mock_user_repository(user)
        email_sender = AsyncMock()

        command = ForgotPasswordCommand(email)
        sut = ForgotPasswordHandler(
            user_repository,
            PyJWTTokenManager('secret'),
            Mock(),
            email_sender,
        )

        # Act
        await sut.handle(command)

        # Assert
        email_sender.send_message.assert_called_once()

    async def test_new_password_command(self) -> None:
        # Arrange
        new_password = same_password ='new_unprotected'
        new_protected_password = 'new_protected'
        user = User(
            uuid4(),
            'test@mail.ru',
            'protected',
            True
        )
        user_repository = self.mock_user_repository(user)
        password_service = self.mock_password_service(
            new_protected_password
        )
        web_session_repository = AsyncMock()

        command = NewPasswordCommand(
            'jwt_token',
            new_password,
            same_password
        )
        sut = NewPasswordHandler(
            user_repository,
            Mock(),
            web_session_repository,
            password_service
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.password == new_protected_password
        web_session_repository \
            .delete_all_with_user_id \
            .assert_called_once_with(user.user_id)


    async def test_user_activate_command(self) -> None:
        # Arrange
        user = User(
            uuid4(),
            'test@mail.ru',
            'protected',
            True
        )
        user_repository = self.mock_user_repository(user)

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

    def mock_user_repository(
        self, 
        return_value: User
    ) -> UserRepository:
        user_repository = AsyncMock()
        user_repository.with_id = AsyncMock(
            return_value=return_value
        )
        user_repository.with_email = AsyncMock(
            return_value=return_value
        )
        return user_repository
    
    def mock_password_service(
        self,
        return_value: str
    ) -> PasswordChangeService:
        password_hasher = Mock()
        password_hasher.hash = Mock(
            return_value=return_value
        )
        password_service = PasswordChangeService(
            password_hasher
        )
        return password_service