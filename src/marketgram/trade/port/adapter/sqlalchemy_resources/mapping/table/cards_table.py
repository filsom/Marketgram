from sqlalchemy import (
    DECIMAL, 
    DateTime,
    Integer,
    String, 
    Table, 
    Column, 
    ForeignKey,
    BigInteger
)
from sqlalchemy.dialects.postgresql import JSONB

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.trade.domain.model.types import INFINITY


cards_table = Table(
    'cards',
    metadata,
    Column('card_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('owner_id', BigInteger, ForeignKey('members.member_id'), index=True, nullable=False),
    Column('category_id', BigInteger, ForeignKey('categories.category_id'), index=True, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('init_price', DECIMAL(20, 2), nullable=False),
    Column('features', JSONB, nullable=True),
    Column('shipping_hours', Integer, nullable=False),
    Column('inspection_hours', Integer, nullable=False),
    Column('shipment', String(20), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('status', String, nullable=False),
)


cards_descriptions_table = Table(
    'cards_descriptions',
    metadata,
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), primary_key=True, nullable=False),
    Column('description_id', BigInteger, ForeignKey('descriptions.description_id'), primary_key=True, nullable=False),
)


descriptions_table = Table(
    'descriptions',
    metadata,
    Column('description_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('card_id', BigInteger, ForeignKey('cards.card_id'), index=True, nullable=False),
    Column('name', String, nullable=False),
    Column('body', String, nullable=False),
    Column('status', String, nullable=False),
    Column('set_in', DateTime(timezone=True), nullable=True),
    Column('archived_in', DateTime(timezone=True), nullable=False, default=INFINITY),
)
