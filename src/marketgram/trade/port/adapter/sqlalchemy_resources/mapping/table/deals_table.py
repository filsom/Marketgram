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

from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.types import (
    BIGSERIAL
)
from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


deals_table = Table(
    'deals',
    sqlalchemy_metadata,
    Column('deal_id', BIGSERIAL, primary_key=True, nullable=False, autoincrement=True),
    Column('card_id', BIGSERIAL, ForeignKey('cards.card_id'), nullable=False),
    Column('qty_purchased', Integer, nullable=False),
    Column('type', String, nullable=False),
    Column('card_created_at', DateTime, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('shipped_at', DateTime(timezone=True), nullable=True),
    Column('received_at', DateTime(timezone=True), nullable=True),
    Column('closed_at', DateTime(timezone=True), nullable=True),
    Column('shipping_hours', Integer, nullable=True),
    Column('receipt_hours', Integer, nullable=True),
    Column('check_hours', Integer, nullable=True),
    Column('status', String, nullable=True),
    Column('is_disputed', Boolean, default=False, nullable=True)
)


deals_members_table = Table(
    'deals_members',
    sqlalchemy_metadata,
    Column('deal_id', BIGSERIAL, ForeignKey('deals.deal_id'), primary_key=True, nullable=False),
    Column('seller_id', UUID, ForeignKey('members.user_id'), primary_key=True, nullable=False),
    Column('buyer_id', UUID, ForeignKey('members.user_id'), primary_key=True, nullable=False),
)


deals_entries_table = Table(
    'deals_entries',
    sqlalchemy_metadata,
    Column('deal_id', BIGSERIAL, ForeignKey('deals.deal_id'), primary_key=True, nullable=False),
    Column('entry_id', UUID, ForeignKey('entries.entry_id'), primary_key=True, nullable=False),
)