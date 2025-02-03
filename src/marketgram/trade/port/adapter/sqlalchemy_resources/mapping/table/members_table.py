from sqlalchemy import UUID, Boolean, Integer, String, Table, Column

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


members_table = Table(
    'members',
    metadata,
    Column('member_id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('user_id', UUID, unique=True, nullable=False),
    Column('synonym', String, nullable=True),
    Column('first6', String, nullable=True),
    Column('last4', String, nullable=True),
    Column('is_blocked', Boolean, default=False, nullable=False),
)