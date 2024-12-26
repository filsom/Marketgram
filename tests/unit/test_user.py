from uuid import uuid4

from marketgram.identity.access.domain.model.user import User


class TestUser:
    def test_create_user(self) -> None:
        # Arrange
        email = 'test@test.ru'
        password = 'unprotected'

        # Act
        sut = User(uuid4(), email, password)

        # Assert
        assert sut.password != password