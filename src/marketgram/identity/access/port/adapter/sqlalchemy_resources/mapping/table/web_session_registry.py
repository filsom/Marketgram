from sqlalchemy.orm import registry

from marketgram.identity.access.domain.model.web_session import WebSession
from marketgram.identity.access.port.adapter.sqlalchemy_resources.mapping.table.web_session_table import (
    web_session_table
)

def web_session_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        WebSession, 
        web_session_table,
        properties={
            'session_id': web_session_table.c.session_id,
            'user_id': web_session_table.c.user_id,
            'created_at': web_session_table.c.created_at,
            'expires_in': web_session_table.c.expires_in,
            'device': web_session_table.c.device
        },
        version_id_col=web_session_table.c.version_id,
    )