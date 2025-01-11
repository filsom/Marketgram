from uuid import uuid4

from marketgram.identity.access.domain.model.authentication_service import (
    AuthenticationService
)
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.argon2_password_hasher import (
    Argon2PasswordHasher
)


class TestAuthenticationService:
    def test_successful_authenticate(self) -> None:
        # Arrange
        email = 'test@mail.ru'
        password = 'unprotected'
        password_hasher = Argon2PasswordHasher()

        user = User(
            uuid4(),
            email,
            password_hasher.hash(password)

        )
        user.activate()

        sut = AuthenticationService(password_hasher)

        # Act
        sut.authenticate(user, password)