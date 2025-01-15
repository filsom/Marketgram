from sqlalchemy.orm import registry

from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.roles_table import (
    role_table
)


def roles_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Role,
        role_table,
        properties={
            '_user_id': role_table.c.user_id,
            '_permission': role_table.c.permission,
        }
    )