from sqlalchemy import (
    DECIMAL, 
    UUID,
    Boolean,
    DateTime,
    String, 
    Table, 
    Column, 
    ForeignKey,
    BigInteger
)

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import sqlalchemy_metadata


cards_table = Table(
    'cards',
    sqlalchemy_metadata,
    Column('card_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('owner_id', UUID, ForeignKey('members.user_id'), index=True, nullable=False),
    Column('price', DECIMAL(20, 2), nullable=False),
    Column('title', String, nullable=False),
    Column('text_description', String, nullable=False),
    Column('account_format', String, nullable=False),
    Column('region', String, nullable=False),
    Column('spam_block', Boolean, nullable=False),
    Column('format', String, nullable=False),
    Column('method', String, nullable=False),
    Column('min_price', DECIMAL(20, 2), nullable=False),
    Column('min_discount', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('dirty_price', DECIMAL(20, 2), nullable=True),
    Column('is_archived', Boolean, default=False, nullable=False),
    Column('is_purchased', Boolean, default=False, nullable=False)
)
