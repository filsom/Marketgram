from uuid import UUID

from marketgram.identity.access.domain.model.access.role_permission import Permission


class Role:
    def __init__(
        self,
        user_id: UUID,
        permission: Permission
    ) -> None:
        self._user_id = user_id
        self._permission = permission
    
    @property
    def permission(self) -> str:
        return self._permission.value