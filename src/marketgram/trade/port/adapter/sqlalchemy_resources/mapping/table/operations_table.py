from sqlalchemy import (
    DDL,
    DECIMAL, 
    UUID, 
    Boolean, 
    Column, 
    DateTime, 
    ForeignKey, 
    Integer, 
    String, 
    Table, 
    event,
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


operations_table = Table(
    'operations',
    metadata,
    Column('operation_id', UUID, primary_key=True, nullable=False),
    Column('user_id', UUID, ForeignKey('members.user_id'), index=True, nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('is_processed', Boolean, nullable=False),
    Column('is_blocked', Boolean, nullable=False),
    Column('count_block', Integer, default=0, nullable=False),
    Column('paycard_synonym', String, nullable=True),
    Column('type', String, nullable=False),
)


func = DDL(
    "CREATE UNIQUE INDEX ON operations(user_id) WHERE NOT is_processed AND type = 'payout'"
)
event.listen(operations_table, 'after_create', func.execute_if(dialect="postgresql"))