from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand, 
    PasswordChange
)
from marketgram.identity.access.application.commands.forgotten_password import (
    ForgottenPasswordCommand, 
    ForgottenPassword
)
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand, 
    NewPassword
)
from marketgram.identity.access.application.commands.user_activate import (
    UserAcivateCommand, 
    UserActivate
)
from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.application.commands.user_registration import (
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


class TestHandlers:
    async def test_change_password_command(self) -> None:
        # Arrange
        user = self.make_user()
        session_id = uuid4()
        auth_service = AsyncMock()
        auth_service.using_id = AsyncMock(
            return_value=user
        )
        web_session_repository = AsyncMock()
        web_session_repository.lively_with_id = AsyncMock(
            return_value=WebSession(
                user.user_id,
                session_id,
                datetime.now(UTC),
                datetime.now(UTC) + timedelta(days=15),
                'Nokia 3210'
            )
        )
        command = PasswordChangeCommand(
            session_id,
            'old_unprotected',
            'new_unprotected',
            'new_unprotected'
        )
        sut = PasswordChange(
            auth_service,
            self.mock_password_service(
                return_value='new_protected'
            ),
            web_session_repository
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.password == 'new_protected'
        sut._web_session_repository \
            .delete_all_with_user_id \
            .assert_called_once_with(user.user_id)

    async def test_forgot_password_command(self) -> None:
        # Arrange
        user = self.make_user()
        message_maker = Mock()
        email_sender = AsyncMock()

        command = ForgottenPasswordCommand('test@mail.ru')
        sut = ForgottenPassword(
            self.mock_user_repository(return_value=user),
            PyJWTTokenManager('secret'),
            message_maker,
            email_sender
        )

        # Act
        await sut.handle(command)

        # Assert
        sut._email_sender.send_message.assert_called_once()

    async def test_new_password_command(self) -> None:
        # Arrange
        user = self.make_user()
        jwt_manager = PyJWTTokenManager('secret')
        token = jwt_manager.encode({
            'sub': user.to_string_id(),
            'aud': 'user:password'
        })
        web_session_repository = AsyncMock()

        command = NewPasswordCommand(
            token,
            'new_unprotected',
            'new_unprotected'
        )
        sut = NewPassword(
            self.mock_user_repository(return_value=user),
            jwt_manager,
            web_session_repository,
            self.mock_password_service(
                return_value='new_protected'
            )
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.password == 'new_protected'
        sut._web_session_repository \
            .delete_all_with_user_id \
            .assert_called_once_with(user.user_id)


    async def test_user_activate_command(self) -> None:
        # Arrange
        user = self.make_user()
        jwt_manager = PyJWTTokenManager('secret')
        token = jwt_manager.encode({
            'sub': user.to_string_id(),
            'aud':'user:activate'
        }) 
        command = UserAcivateCommand(token)
        sut = UserActivate(
            jwt_manager,
            self.mock_user_repository(return_value=user)
        )

        # Act
        await sut.handle(command)

        # Assert
        assert user.is_active == True

    async def test_user_login_command(self) -> None:
        # Arrange
        user_id = uuid4()
        session_id = str(uuid4())
        days = 15
        created_at = datetime.now(UTC)
        expires_in = created_at + timedelta(days=days)

        auth_service = AsyncMock()
        auth_service.using_email = AsyncMock(
            return_value=User(
                user_id,
                'test@mail.ru',
                'protected',
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
            'test@mail.ru',
            'protected',
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
            'user_id': str(user_id),
            'session_id': str(session_id), 
            'expires_in': expires_in.strftime('%a, %d %b %Y %H:%M:%S')
        } == result

    async def test_user_registration_command(self) -> None:
        # Arrange
        user_id = uuid4()
        user_creation_service = AsyncMock()
        user_creation_service.create = AsyncMock(
            return_value=str(user_id)
        )
        message_maker = Mock()
        email_sender = AsyncMock()

        command = UserRegistrationCommand(
            'test@mail.ru',
            'unprotected',
            'unprotected'
        )
        sut = UserRegistrationHandler(
            user_creation_service,
            PyJWTTokenManager('secret'),
            message_maker,
            email_sender
        )

        # Act
        await sut.handle(command)

        # Assert
        sut._email_sender.send_message.assert_called_once()

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
    
    def make_user(self) -> User:
        return User(
            uuid4(),
            'test@mail.ru',
            'protected',
            True
        )