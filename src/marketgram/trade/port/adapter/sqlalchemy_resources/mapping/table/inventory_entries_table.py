from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    BigInteger,
    ForeignKey,
    Integer,
    String,
    Table,
    text
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


inventory_entries_table = Table(
    'inventory_entries',
    metadata,
    Column('entry_id', UUID, primary_key=True, server_default=text("gen_random_uuid()"), nullable=False),
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), index=True, nullable=False),
    Column('qty', Integer, nullable=False),
    Column('posted_in', DateTime(timezone=True), nullable=False),
    Column('operation', String, nullable=False)
)