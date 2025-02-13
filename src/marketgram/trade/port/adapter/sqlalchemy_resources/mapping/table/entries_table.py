from uuid import uuid4

from sqlalchemy import (
    DECIMAL, 
    UUID, 
    Boolean, 
    DateTime, 
    ForeignKey,
    BigInteger,
    Integer, 
    String, 
    Table, 
    Column,
    text, 
)

from marketgram.common.sqlalchemy_metadata import metadata



entries_table = Table(
    'entries',
    metadata,
    Column('entry_id', UUID, primary_key=True, default=uuid4, nullable=False),
    Column('user_id', UUID, ForeignKey('members.user_id'), index=True, nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('posted_in', DateTime(timezone=True), nullable=False),
    Column('account_type', String, nullable=False),
    Column('operation', String, nullable=False),
    Column('entry_status', String, nullable=False),
    Column('is_archived', Boolean, default=False, nullable=False)
)


inventory_entries_table = Table(
    'inventory_entries',
    metadata,
    Column('entry_id', UUID, primary_key=True, server_default=text("gen_random_uuid()"), nullable=False),
    Column('qty', Integer, nullable=False),
    Column('posted_in', DateTime(timezone=True), nullable=False),
    Column('operation', String, nullable=False)
)


cards_inventory_entries_table = Table(
    'cards_inventory_entries',
    metadata,
    Column('entry_id', UUID, ForeignKey('inventory_entries.entry_id'), primary_key=True, nullable=False),
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), primary_key=True, nullable=False),
)