from uuid import uuid4
from sqlalchemy import (
    DECIMAL, 
    UUID, 
    Boolean, 
    DateTime, 
    ForeignKey,
    BigInteger, 
    String, 
    Table, 
    Column, 
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata



entries_table = Table(
    'entries',
    metadata,
    Column('entry_id', UUID, primary_key=True, default=uuid4, nullable=False),
    Column('member_id', BigInteger, ForeignKey('members.member_id'), index=True, nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('posted_in', DateTime(timezone=True), nullable=False),
    Column('account_type', String, nullable=False),
    Column('operation', String, nullable=False),
    Column('entry_status', String, nullable=False),
    Column('is_archived', Boolean, nullable=False)
)