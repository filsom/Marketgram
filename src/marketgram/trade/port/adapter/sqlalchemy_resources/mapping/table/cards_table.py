from sqlalchemy import (
    DECIMAL,
    UUID, 
    DateTime,
    Enum,
    Integer,
    String, 
    Table, 
    Column, 
    ForeignKey,
    BigInteger
)
from sqlalchemy.dialects.postgresql import JSONB

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.types import INFINITY


cards_table = Table(
    'cards',
    metadata,
    Column('card_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('owner_id', UUID, ForeignKey('members.user_id'), index=True, nullable=False),
    Column('category_id', BigInteger, ForeignKey('categories.category_id'), index=True, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('init_price', DECIMAL(20, 2), nullable=False),
    Column('features', JSONB, nullable=True),
    Column('shipping_hours', Integer, nullable=False),
    Column('inspection_hours', Integer, nullable=False),
    Column('shipment', Enum(Shipment), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('status', Enum(StatusCard, native_enum=False), nullable=False),
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
