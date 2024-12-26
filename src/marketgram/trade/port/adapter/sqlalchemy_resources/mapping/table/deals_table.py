from uuid import uuid4
from sqlalchemy import (
    DECIMAL, 
    UUID,
    Boolean,
    DateTime,
    Integer, 
    String, 
    Table, 
    Column, 
    ForeignKey,
)

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


deals_table = Table(
    'deals',
    sqlalchemy_metadata,
    Column('deal_id', UUID, primary_key=True, nullable=False, default=uuid4),
    Column('seller_id', UUID, ForeignKey('members.user_id'), nullable=False),
    Column('buyer_id', UUID, ForeignKey('members.user_id'), nullable=False),
    Column('card_id', UUID, nullable=False),
    Column('qty_purchased', Integer, nullable=False),
    Column('type', String, nullable=False),
    Column('card_created_at', DateTime, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('shipped_at', DateTime, nullable=True),
    Column('received_at', DateTime, nullable=True),
    Column('closed_at', DateTime, nullable=True),
    Column('shipping_hours', Integer, nullable=True),
    Column('receipt_hours', Integer, nullable=True),
    Column('check_hours', Integer, nullable=True),
    Column('status', String, nullable=True),
    Column('is_disputed', Boolean, default=False, nullable=True)
)


deals_entries_table = Table(
    'deals_entries',
    sqlalchemy_metadata,
    Column('deal_id', UUID, ForeignKey('deals.deal_id'), nullable=False),
    Column('entry_id', UUID, ForeignKey('entries.entry_id'), nullable=False),
)