from sqlalchemy import (
    DECIMAL, 
    UUID, 
    Boolean, 
    DateTime, 
    ForeignKey, 
    String, 
    Table, 
    Column, 
    text
)

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


entries_table = Table(
    'entries',
    sqlalchemy_metadata,
    Column(
        'entry_id', 
        UUID, 
        primary_key=True, 
        server_default=text("gen_random_uuid()"), 
        nullable=False
    ),
    Column('user_id', UUID, ForeignKey('members.user_id'), nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('posted_in', DateTime, nullable=False),
    Column('account_type', String, nullable=False),
    Column('operation', String, nullable=False),
    Column('entry_status', String, nullable=False),
    Column('is_archived', Boolean, nullable=False)
)