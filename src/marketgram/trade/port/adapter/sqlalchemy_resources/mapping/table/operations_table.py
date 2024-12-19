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
    text,
    event
)

from marketgram.trade.port.adapter.sqlalchemy_resources.metadata import (
    sqlalchemy_metadata
)


operations_table = Table(
    'operations',
    sqlalchemy_metadata,
    Column('operation_id', UUID, primary_key=True, nullable=False),
    Column('user_id', UUID, ForeignKey('members.user_id'), nullable=False),
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


operations_entries_table = Table(
    'operations_entries',
    sqlalchemy_metadata,
    Column('operation_id', UUID, ForeignKey('operations.operation_id'), nullable=False),
    Column('entry_id', UUID, ForeignKey('entries.entry_id'), nullable=False)
)