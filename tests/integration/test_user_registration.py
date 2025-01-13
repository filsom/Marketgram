# from unittest.mock import AsyncMock

# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession

# from marketgram.common.application.message_renderer import MessageRenderer
# from marketgram.identity.access.application.commands.user_registration import (
#     UserRegistrationCommand, 
#     UserRegistrationHandler
# )
# from marketgram.identity.access.port.adapter.argon2_password_hasher import (
#     Argon2PasswordHasher
# )
# from marketgram.identity.access.port.adapter.pyjwt_token_manager import (
#     PyJWTTokenManager
# )
# from marketgram.identity.access.port.adapter.sqlalchemy_resources.role_repository import (
#     RoleRepository
# )
# from marketgram.identity.access.port.adapter.sqlalchemy_resources.user_repository import (
#     UserRepository
# )
# from marketgram.identity.access.settings import ActivateHtmlSettings, JWTManagerSecret


# @pytest.mark.asyncio
# @pytest.mark.parametrize('email,password', [('test@mail.ru', 'unprotected')])
# async def test_user_registration(
#     email: str, 
#     password: str,
#     async_session: AsyncSession,
#     activate_msg_renderer: MessageRenderer[ActivateHtmlSettings, str]
# ) -> None:
#     # Arrange
#     email_sender = AsyncMock()

#     sut = UserRegistrationHandler(
#         UserRepository(async_session),
#         RoleRepository(async_session),
#         PyJWTTokenManager(JWTManagerSecret('secret')),
#         activate_msg_renderer,
#         email_sender,
#         Argon2PasswordHasher()
#     )

#     # Act
#     result = await sut.handle(UserRegistrationCommand(email, password))

#     # Assert
#     user_repository = UserRepository(async_session)
#     role_repository = RoleRepository(async_session)
#     user = await user_repository.with_email('test@mail.ru')

#     assert result == None
#     assert user.email == email
#     assert user.password != password
#     assert user.is_active == False
#     sut._email_sender.send_message.assert_called_once()