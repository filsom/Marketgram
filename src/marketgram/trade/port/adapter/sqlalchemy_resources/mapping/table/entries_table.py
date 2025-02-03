from uuid import uuid4
from sqlalchemy import (
    DECIMAL, 
    UUID, 
    Boolean, 
    DateTime, 
    ForeignKey,
    Integer, 
    String, 
    Table, 
    Column, 
)

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


entries_table = Table(
    'entries',
    sqlalchemy_metadata,
    Column('entry_id', UUID, primary_key=True, default=uuid4, nullable=False),
    Column('member_id', Integer, ForeignKey('members.member_id'), nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('posted_in', DateTime, nullable=False),
    Column('account_type', String, nullable=False),
    Column('operation', String, nullable=False),
    Column('entry_status', String, nullable=False),
    Column('is_archived', Boolean, nullable=False)
)