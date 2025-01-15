from sqlalchemy import UUID, Boolean, Column, Integer, String, Table

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata

user_table = Table(
    'users',
    metadata,
    Column('user_id', UUID, primary_key=True, nullable=False),
    Column('email', String(100), unique=True, nullable=False),
    Column('password', String(100), nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('version_id', Integer, nullable=False)
)