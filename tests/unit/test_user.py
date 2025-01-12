from uuid import uuid4

import pytest

from marketgram.identity.access.domain.model.errors import PersonalDataError
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_factory import UserFactory
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)


@pytest.fixture
def password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher(
        time_cost=2,
        memory_cost=19 * 1024,
        parallelism=1
    )


class TestUser:
    def test_create_new_user(
        self, 
        password_hasher: Argon2PasswordHasher
    ) -> None:
        # Arrange
        email = 'test@mail.ru'
        password = 'unprotected'

        sut = UserFactory(password_hasher)

        # Act
        new_user = sut.create(email, password)

        # Assert
        assert password_hasher.verify(new_user.password, password)
        assert new_user.email.islower()

    def test_create_new_user_with_same_password_and_email(
        self, 
        password_hasher: Argon2PasswordHasher
    )-> None:
        # Arrange
        email = 'test@mail.ru'
        password = 'test@mail.ru'

        sut = UserFactory(password_hasher)

        # Act
        with pytest.raises(PersonalDataError):
            sut.create(email, password)

    def test_change_user_password(
        self, 
        password_hasher: Argon2PasswordHasher
    )-> None:
        # Arrange
        new_password = 'new_unprotected' 
        
        sut = User(
            uuid4(), 
            'test@mail.ru', 
            password_hasher.hash('old_protected')
        )
        sut.activate()

        # Act
        sut.change_password(new_password, password_hasher)

        # Assert
        assert password_hasher.verify(sut.password, new_password)

    def test_inactive_user_password_change(
        self, 
        password_hasher: Argon2PasswordHasher
    )-> None:
        # Arrange
        new_password = 'new_unprotected'

        sut = User(
            uuid4(), 
            'test@mail.ru', 
            password_hasher.hash('old_protected')
        )

        # Act
        with pytest.raises(PersonalDataError):
            sut.change_password(new_password, password_hasher)

        # Assert
        assert not password_hasher.verify(sut.password, new_password)
 
    def test_changing_password_when_email_matches(
        self, 
        password_hasher: Argon2PasswordHasher
    )-> None:
        # Arrange
        new_password = 'test@mail.ru'

        sut = User(
            uuid4(), 
            'test@mail.ru', 
            password_hasher.hash('old_protected')
        )
        
        # Act
        with pytest.raises(PersonalDataError):
            sut.change_password(new_password, password_hasher)

        # Act
        assert not password_hasher.verify(sut.password, new_password)

    def test_user_activation(self) -> None:
        # Arrange
        sut = User(uuid4(), 'test@mail.ru', 'old_protected')

        # Act
        sut.activate()

        # Assert
        assert True == sut.is_active