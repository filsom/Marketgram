from sqlalchemy import UUID, Boolean, Integer, String, Table, Column

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


members_table = Table(
    'members',
    sqlalchemy_metadata,
    Column('member_id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('user_id', UUID, unique=True, nullable=False),
    Column('synonym', String, nullable=True),
    Column('first6', String, nullable=True),
    Column('last4', String, nullable=True),
    Column('is_blocked', Boolean, default=False, nullable=False),
)