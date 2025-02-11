from sqlalchemy import Column, Enum, ForeignKey, Table, UUID,text

from marketgram.common.sqlalchemy_metadata import metadata
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
    Column('user_id', UUID, ForeignKey('users.user_id'), nullable=False),
    Column('permission', Enum(Permission), nullable=False),
)