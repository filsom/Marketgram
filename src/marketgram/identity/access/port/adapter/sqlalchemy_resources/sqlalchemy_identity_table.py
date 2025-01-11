from sqlalchemy import (
    Boolean, 
    Column, 
    DateTime, 
    Enum, 
    Integer,
    String, 
    Table, 
    UUID,
    text
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.identity.access.domain.model.role_permission import Permission


user_table = Table(
    'users',
    metadata,
    Column('user_id', UUID, primary_key=True, nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('password', String(100), nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('version_id', Integer, nullable=False)
)


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


web_session_table = Table(
    'web_session',
    metadata,
    Column(
        'id', 
        UUID, 
        primary_key=True, 
        nullable=False, 
        server_default=text("gen_random_uuid()")
    ),
    Column('session_id', UUID, nullable=False),
    Column('user_id', UUID, nullable=False, unique=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('expires_in', DateTime(timezone=True), nullable=False),
    Column('device', String, nullable=False),
    Column('version_id', Integer, nullable=False)
)