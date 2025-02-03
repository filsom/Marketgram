from uuid import uuid4
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Integer,
    String,
    Table
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


inventory_entries_table = Table(
    'inventory_entries',
    metadata,
    Column('entry_id', UUID, primary_key=True, default=uuid4, nullable=False),
    Column('qty', Integer, nullable=False),
    Column('posted_in', DateTime(timezone=True), nullable=False),
    Column('operation', String, nullable=False)
)