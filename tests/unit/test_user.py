from unittest.mock import Mock, AsyncMock
from uuid import uuid4

import pytest

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD,
    DomainError
)
from marketgram.identity.access.domain.model.password_change_service import (
    PasswordChangeService
)
from marketgram.identity.access.domain.model.password_security_hasher import (
    PasswordSecurityHasher
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_authentication_service import (
    UserAuthenticationService
)
from marketgram.identity.access.domain.model.user_creation_service import (
    UserCreationService
)


class TestUser:
    async def test_user_authentication_using_email(self) -> None:
        # Arrange
        user_id = uuid4()
        email = 'test@mail.ru'
        password = 'protected'

        user_repository = AsyncMock()
        user_repository.with_email = AsyncMock(
            return_value=User(
                user_id,
                email,
                password,
                True
            )
        )
        sut = UserAuthenticationService(
            user_repository,
            self.mock_password_hasher()
        )

        # Act
        result = await sut.using_email(
            email,
            password
        )

        # Assert
        assert user_id == result.user_id

    async def test_create_user(self) -> None:
        # Arrange
        user_id = uuid4()

        user_repository = AsyncMock() 
        user_repository.next_identity = Mock(return_value=user_id)
        user_repository.add = AsyncMock()
        user_repository.with_email = AsyncMock(return_value=None)

        role_repository = AsyncMock()
        role_repository.add = AsyncMock()

        sut = UserCreationService(
            user_repository,
            role_repository,
            self.mock_password_hasher()
        )

        # Act
        result = await sut.create(
            'test@mail.ru',
            'unprotected',
            'unprotected'
        )

        # Assert
        assert str(user_id) == result


    def test_change_password(self) -> None:
        # Arrange
        sut = self.make_user('test@mail.ru', True)
        password_service = PasswordChangeService(
            self.mock_password_hasher()
        )

        # Act
        password_service.change(sut, 'unprotected', 'unprotected')

        # Assert
        assert sut.password == 'protected'

    @pytest.mark.parametrize(
        'email,password,same_password', [
            ('test@mail.ru', 'test@mail.ru', 'test@mail.ru'),
            ('test@mail.ru', 'unprotected', 'unprotected_v2')
        ]
    )
    def test_incorrect_email_and_password(
        self, 
        email: str, 
        password: str, 
        same_password: str
    ) -> None:
        # Arrange
        sut = self.make_user(email, True)
        password_service = PasswordChangeService(
            self.mock_password_hasher()
        )

        # Act
        with pytest.raises(DomainError) as excinfo:
            password_service.change(sut, password, same_password)

        # Assert
        assert INVALID_EMAIL_OR_PASSWORD == str(excinfo.value)

    def make_user(self, email: str, is_active: bool = False):
        return User(
            uuid4(),
            email,
            'protected',
            is_active
        )
    
    def mock_password_hasher(
        self, 
        return_value: str = 'protected'
    ) -> PasswordSecurityHasher:
        password_hasher = Mock()
        password_hasher.hash = Mock(return_value=return_value)
        password_hasher.verify = self.verify
        password_hasher.check_needs_rehash = Mock(return_value=False)

        return password_hasher
    
    def verify(self, plain_password, password):
        return plain_password == password