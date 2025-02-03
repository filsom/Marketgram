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
    BigInteger
)

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata


operations_table = Table(
    'operations',
    metadata,
    Column('operation_id', UUID, primary_key=True, nullable=False),
    Column('member_id', BigInteger, ForeignKey('members.member_id'), index=True, nullable=False),
    Column('amount', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('is_processed', Boolean, nullable=False),
    Column('is_blocked', Boolean, nullable=False),
    Column('count_block', Integer, default=0, nullable=False),
    Column('paycard_synonym', String, nullable=True),
    Column('type', String, nullable=False),
)


func = DDL(
    "CREATE UNIQUE INDEX ON operations(member_id) WHERE NOT is_processed AND type = 'payout'"
)
event.listen(operations_table, 'after_create', func.execute_if(dialect="postgresql"))


operations_entries_table = Table(
    'operations_entries',
    metadata,
    Column('operation_id', UUID, ForeignKey('operations.operation_id'), nullable=False),
    Column('entry_id', UUID, ForeignKey('entries.entry_id'), nullable=False)
)