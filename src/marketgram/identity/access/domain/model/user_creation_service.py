from marketgram.identity.access.domain.model.exceptions import INVALID_EMAIL_OR_PASSWORD, DomainError
from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.role_permission import Permission
from marketgram.identity.access.domain.model.role_repository import RoleRepository
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.domain.model.user_repository import UserRepository


class UserCreationService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository

    async def create(self, email: str, password: str) -> str:
        exists_user = await self._user_repository \
            .with_email(email)
        
        if exists_user is not None:
            raise DomainError(INVALID_EMAIL_OR_PASSWORD)
        
        new_user = User(
            self._user_repository.next_identity(),
            email.lower(),
            password
        )
        role_for_user = Role(
            new_user.user_id,
            Permission.USER
        )
        await self._user_repository.add(new_user)
        await self._role_repository.add(role_for_user)

        return new_user.to_string_id(), new_user.email 