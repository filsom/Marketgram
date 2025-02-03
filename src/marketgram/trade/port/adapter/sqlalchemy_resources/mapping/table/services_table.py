from sqlalchemy import String, Table, Column, BigInteger

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import sqlalchemy_metadata


services_table = Table(
    'services',
    sqlalchemy_metadata,
    Column('service_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('name', String, nullable=False),
    Column('alias', String, nullable=False),
)