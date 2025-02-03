from sqlalchemy import DECIMAL, DateTime, ForeignKey, Table, Column, BigInteger

from marketgram.common.port.adapter.sqlalchemy_metadata import metadata
from marketgram.trade.domain.model.types import INFINITY


service_agreements_table = Table(
    'service_agreements',
    metadata,
    Column('agreement_id', BigInteger, primary_key=True, nullable=False, autoincrement=True),
    Column('manager_id', BigInteger, ForeignKey('members.user_id'), index=True, nullable=False),
    Column('payout_tax', DECIMAL(20, 2), nullable=False),
    Column('sales_tax', DECIMAL(20, 2), nullable=False),
    Column('minimum_payout', DECIMAL(20, 2), nullable=False),
    Column('minimum_payment', DECIMAL(20, 2), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('archived_in', DateTime(timezone=True), nullable=True, default=INFINITY),
)