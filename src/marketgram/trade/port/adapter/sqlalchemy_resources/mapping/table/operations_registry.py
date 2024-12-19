from sqlalchemy.orm import registry, relationship, composite

from marketgram.trade.domain.model.p2p.payment import Payment
from marketgram.trade.domain.model.p2p.payout import Payout
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.operations_table import (
    operations_table,
    operations_entries_table
)



def operations_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        Payout,
        operations_table,
        polymorphic_on=operations_table.c.type,
        polymorphic_identity='payout',
        properties={
            '_payout_id': operations_table.c.operation_id,
            '_user_id': operations_table.c.user_id,
            '_paycard_synonym': operations_table.c.paycard_synonym,
            '_tax_free': composite(Money, operations_table.c.amount),
            '_created_at': operations_table.c.created_at,
            '_count_block': operations_table.c.count_block,
            '_is_processed': operations_table.c.is_processed,
            '_is_blocked': operations_table.c.is_blocked,
            '_entries': relationship(
                'PostingEntry',
                secondary=operations_entries_table,
                default_factory=list,
                lazy='subquery',
                overlaps='_entries'
            )
        }
    )
    mapper.map_imperatively(
        Payment,
        operations_table,
        polymorphic_on=operations_table.c.type,
        polymorphic_identity='payment',
        properties={
            '_payment_id': operations_table.c.operation_id,
            '_user_id': operations_table.c.user_id,
            '_amount': composite(Money, operations_table.c.amount),
            '_created_at': operations_table.c.created_at,
            '_is_processed': operations_table.c.is_processed,
            '_is_blocked': operations_table.c.is_blocked,
            '_entries': relationship(
                'PostingEntry',
                secondary=operations_entries_table,
                default_factory=list,
                lazy='noload',
                overlaps='_entries'
            )
        },
    )