from sqlalchemy import Column, Enum, Table, UUID,text

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.identity.access.domain.model.role_permission import Permission


role_table = Table(
    'roles',
    metadata,
    Column(
        'role_id', 
        UUID, 
        primary_key=True, 
        nullable=False, 
        server_default=text("gen_random_uuid()")
    ),
    Column('user_id', UUID, nullable=False, unique=True),
    Column('permission', Enum(Permission), nullable=False),
)