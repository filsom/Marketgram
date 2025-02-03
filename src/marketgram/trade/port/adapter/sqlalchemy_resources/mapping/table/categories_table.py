from sqlalchemy import (
    DECIMAL,
    BigInteger, 
    Column,
    DateTime, 
    ForeignKey, 
    Integer, 
    String, 
    Table
)

from marketgram.common.port.adapter import sqlalchemy_metadata


categories_table = Table(
    'deals',
    sqlalchemy_metadata,
    Column('category_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), nullable=False),
    Column('qty_purchased', Integer, nullable=False),
    Column('shipment', String, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('status', String, nullable=True),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('shipped_at', DateTime(timezone=True), nullable=True),
    Column('inspected_at', DateTime(timezone=True), nullable=True),
    Column('ship_to', DateTime(timezone=True), nullable=False), 
    Column('inspect_to', DateTime(timezone=True), nullable=False),
    Column('download_link', String, nullable=True),
)