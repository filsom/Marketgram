from uuid import uuid4

import pytest

from marketgram.identity.access.domain.model.exceptions import (
    INVALID_EMAIL_OR_PASSWORD, 
    PasswordError
)
from marketgram.identity.access.domain.model.user import User


class TestUser:
    def test_new_user(self) -> None:
        # Arrange
        email = 'test@test.ru'
        password = 'unprotected'

        # Act
        sut = User(uuid4(), email, password)

        # Assert
        assert sut.password != password

    def test_creating_user_with_identical_password_and_email(self) -> None:
        # Arrange
        email = 'test@test.ru'
        password = 'test@test.ru'

        # Act
        with pytest.raises(PasswordError) as excinfo:
            User(uuid4(), email, password)

        # Assert
        assert INVALID_EMAIL_OR_PASSWORD == str(excinfo.value)