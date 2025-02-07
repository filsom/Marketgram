from sqlalchemy import UUID, Boolean, String, Table, Column, BigInteger

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


members_table = Table(
    'members',
    metadata,
    Column('user_id', UUID, primary_key=True, nullable=False),
    Column('member_id', BigInteger, index=True, autoincrement=True, nullable=False),
    Column('synonym', String, nullable=True),
    Column('first6', String, nullable=True),
    Column('last4', String, nullable=True),
    Column('is_blocked', Boolean, default=False, nullable=False),
)