from datetime import UTC, datetime
from uuid import UUID

from marketgram.identity.access.application.commands import (
    AuthenticateUserCommand,
    ChangePasswordCommand,
    SetNewPasswordCommand, 
    UserCreationCommand
)
from marketgram.identity.access.application.identity_service import IdentityService
from marketgram.identity.access.domain.model.role_permission import Permission
from tests.integration.identity.access.conftest import (
    create_user,
    create_web_session,
    delete_all,
    query_count_web_sessions, 
    query_role, 
    query_user_with_email,
    query_user_with_id,
    query_web_session
)


async def test_create_new_user(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)

    # Act
    await service.create_user(UserCreationCommand('Test@mail.ru', 'qwerty'))
        
    # Assert
    service.email_sender.send_message.assert_called_once()

    user_from_db = await query_user_with_email(engine, 'test@mail.ru')
    role_from_db = await query_role(engine, user_from_db.user_id)
    
    assert user_from_db is not None
    assert user_from_db.email == 'test@mail.ru'
    assert not user_from_db.is_active
    assert service.password_hasher.verify(user_from_db.password, 'qwerty')
    assert role_from_db.permission == Permission.USER


async def test_authenticate_activated_user(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)
    await create_user(engine)

    # Act
    result = await service.authenticate_user(
        AuthenticateUserCommand('test@mail.ru', 'qwerty', 'Nokia 3210')
    )

    # Assert
    web_session_from_db = await query_web_session(engine, UUID(result['session_id']))
    
    assert web_session_from_db is not None
    assert web_session_from_db.to_string_id() == result['session_id']
    assert str(web_session_from_db.user_id) == result['user_id']
    assert web_session_from_db.device == 'Nokia 3210'
    assert web_session_from_db.to_formatted_time() == result['expires_in']


async def test_user_activation(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)
    user = await create_user(engine, is_active=False)
    
    activation_token = service.jwt_manager.encode(
        datetime.now(UTC), {'sub': user.to_string_id(), 'aud': 'user:activate'}
    )

    # Act
    await service.activate_user(activation_token)

    # Assert
    user_from_db = await query_user_with_id(engine, user.user_id)

    assert user_from_db is not None
    assert user_from_db.is_active


async def test_activated_user_changes_password(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)
    
    user = await create_user(engine)
    web_session = await create_web_session(engine, user.user_id)

    # Act
    await service.change_user_password(
        ChangePasswordCommand(web_session.session_id, 'qwerty', 'new_qwerty')
    )

    # Assert
    user_from_db = await query_user_with_id(engine, user.user_id)
    count_web_sessions = await query_count_web_sessions(engine, user_from_db.user_id)

    assert user_from_db is not None
    assert service.password_hasher.verify(user_from_db.password, 'new_qwerty')
    assert count_web_sessions == 0


async def test_activated_user_changes_password_using_token(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)

    user = await create_user(engine)
    await create_web_session(engine, user.user_id)

    password_change_token = service.jwt_manager.encode(
        datetime.now(UTC), {'sub': user.to_string_id(), 'aud': 'user:password'}
    )

    # Act
    await service.set_new_password(SetNewPasswordCommand(password_change_token, 'new_qwerty'))

    # Assert
    user_from_db = await query_user_with_id(engine, user.user_id)
    count_web_sessions = await query_count_web_sessions(engine, user_from_db.user_id)

    assert user_from_db is not None
    assert service.password_hasher.verify(user_from_db.password, 'new_qwerty')
    assert count_web_sessions == 0


async def test_activated_user_forgot_password(engine, service: IdentityService) -> None:
        # Arrange
        await delete_all(engine)
        await create_user(engine)

        # Act
        await service.user_forgot_password('test@mail.ru')

        # Assert 
        service.email_sender.send_message.assert_called_once()


async def test_non_activated_user_forgot_password(engine, service: IdentityService) -> None:
    # Arrange
    await delete_all(engine)
    await create_user(engine, is_active=False)

    # Act
    await service.user_forgot_password('test@mail.ru')

    # Assert 
    service.email_sender.send_message.assert_not_called()