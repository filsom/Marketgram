from sqlalchemy import String, Table, Column, BigInteger

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


services_table = Table(
    'services',
    metadata,
    Column('service_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('name', String, nullable=False),
    Column('alias', String, nullable=False),
)