from sqlalchemy import DECIMAL, BigInteger, Column, ForeignKey, Integer, String, Table

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata



category_types_table = Table(
    'category_types',
    metadata,
    Column('type_category_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('name', String(50), nullable=False)
)


categories_table = Table(
    'categories',
    metadata,
    Column('category_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('service_id', BigInteger, ForeignKey('services.service_id'), nullable=False),
    Column('category_type_id', BigInteger, ForeignKey('category_types.type_category_id'), nullable=False),
    Column('alias', String(50), nullable=False),
    Column('shipping_hours', Integer, nullable=False),
    Column('inspection_hours', Integer, nullable=False),
    Column('shipment', String, nullable=False),
    Column('minimum_price', DECIMAL(20, 2), nullable=False),
    Column('minimum_procent_discount', DECIMAL(20, 2), nullable=True),
)