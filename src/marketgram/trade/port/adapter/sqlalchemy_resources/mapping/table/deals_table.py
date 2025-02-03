from sqlalchemy import (
    DECIMAL, 
    UUID,
    DateTime,
    Integer, 
    String, 
    Table, 
    Column, 
    ForeignKey,
    BigInteger
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata



deals_table = Table(
    'deals',
    metadata,
    Column('deal_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), nullable=False),
    Column('qty_purchased', Integer, nullable=False),
    Column('shipment', String(20), nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('status', String, nullable=True),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('shipped_at', DateTime(timezone=True), nullable=True),
    Column('inspected_at', DateTime(timezone=True), nullable=True),
    Column('ship_to', DateTime(timezone=True), nullable=False), 
    Column('inspect_to', DateTime(timezone=True), nullable=False),
    Column('download_link', String, nullable=True),
)


deals_members_table = Table(
    'deals_members',
    metadata,
    Column('deal_id', BigInteger, ForeignKey('deals.deal_id'), primary_key=True, nullable=False),
    Column('seller_id', BigInteger, ForeignKey('members.member_id'), primary_key=True, nullable=False),
    Column('buyer_id', BigInteger, ForeignKey('members.member_id'), primary_key=True, nullable=False),
)


deals_entries_table = Table(
    'deals_entries',
    metadata,
    Column('deal_id', BigInteger, ForeignKey('deals.deal_id'), primary_key=True, nullable=False),
    Column('entry_id', UUID, ForeignKey('entries.entry_id'), primary_key=True, nullable=False),
)