from unittest.mock import Mock
from uuid import uuid4

import pytest

from marketgram.identity.access.domain.model.errors import PersonalDataError
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_factory import UserFactory


def test_create_new_user() -> None:
    # Arrange
    email = 'test@mail.ru'
    password = 'unprotected'

    password_hasher = Mock()
    password_hasher.hash = Mock(return_value='protected')

    sut = UserFactory(password_hasher)

    # Act
    new_user = sut.create(email, password)

    # Assert
    assert 'protected' == new_user.password
    assert new_user.email.islower()


def test_create_new_user_with_same_password_and_email() -> None:
    # Arrange
    email = 'test@mail.ru'
    password = 'test@mail.ru'

    password_hasher = Mock()

    sut = UserFactory(password_hasher)

    # Act
    with pytest.raises(PersonalDataError):
        sut.create(email, password)


def test_change_user_password() -> None:
    # Arrange
    new_password = 'new_unprotected'

    password_hasher = Mock()
    password_hasher.hash = Mock(return_value='new_protected') 

    sut = User(uuid4(), 'test@mail.ru', 'old_protected')
    sut.activate()

    # Act
    sut.change_password(new_password, password_hasher)

    # Assert
    assert 'new_protected' == sut.password


def test_inactive_user_password_change() -> None:
    # Arrange
    new_password = 'new_unprotected'
    password_hasher = Mock()

    sut = User(uuid4(), 'test@mail.ru', 'old_protected')

    # Act
    with pytest.raises(PersonalDataError):
        sut.change_password(new_password, password_hasher)

    # Assert
    assert new_password != sut.password

    
def test_changing_password_when_email_matches() -> None:
    # Arrange
    new_password = 'test@mail.ru'
    password_hasher = Mock()

    sut = User(uuid4(), 'test@mail.ru', 'old_protected')
    
    # Act
    with pytest.raises(PersonalDataError):
        sut.change_password(new_password, password_hasher)

    # Act
    assert new_password != sut.password


def test_user_activation() -> None:
    # Arrange
    sut = User(uuid4(), 'test@mail.ru', 'old_protected')

    # Act
    sut.activate()

    # Assert
    assert True == sut.is_active