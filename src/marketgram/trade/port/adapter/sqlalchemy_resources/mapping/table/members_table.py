from sqlalchemy import UUID, Boolean, String, Table, Column

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


members_table = Table(
    'members',
    sqlalchemy_metadata,
    Column('user_id', UUID, primary_key=True, nullable=False),
    Column('synonym', String, nullable=False),
    Column('first6', String, nullable=False),
    Column('last4', String, nullable=False),
    Column('is_blocked', Boolean, default=False, nullable=False),
)