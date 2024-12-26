from sqlalchemy.orm import registry

from marketgram.identity.access.domain.model.role import Role
from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.domain.model.user import User
from marketgram.identity.access.port.adapter.sqlalchemy_resources.sqlalchemy_identity_table import (
    user_table,
    role_table,
    web_session_table
)


def identity_registry_mapper(mapper_registry: registry):
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            '_user_id': user_table.c.user_id,
            '_email': user_table.c.email,
            '_password': user_table.c.password,
            '_is_active': user_table.c.is_active,
        },
        column_prefix="_",
        version_id_col=user_table.c.version_id,
    )
    mapper_registry.map_imperatively(
        Role,
        role_table,
        properties={
            '_user_id': role_table.c.user_id,
            '_permission': role_table.c.permission,
        }
    )
    mapper_registry.map_imperatively(
        WebSession, 
        web_session_table,
        properties={
            '_session_id': web_session_table.c.session_id,
            '_user_id': web_session_table.c.user_id,
            '_created_at': web_session_table.c.created_at,
            '_expires_in': web_session_table.c.expires_in,
            '_device': web_session_table.c.device
        },
        column_prefix="_",
        version_id_col=web_session_table.c.version_id,
    )