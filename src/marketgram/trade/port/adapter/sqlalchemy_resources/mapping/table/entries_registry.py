from sqlalchemy.orm import registry, composite

from marketgram.trade.domain.model.entries import InventoryEntry, PostingEntry
from marketgram.trade.domain.model.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.inventory_entries_table import (
    inventory_entries_table
)
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.entries_table import (
    entries_table
)


def entries_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        PostingEntry,
        entries_table,
        properties={
            'user_id': entries_table.c.user_id,
            '_amount': entries_table.c.amount,
            'amount': composite(Money, '_amount'),
            'account_type': entries_table.c.account_type,
            'operation': entries_table.c.operation,
            'posted_in': entries_table.c.posted_in,
            'entry_status': entries_table.c.entry_status,
            'is_archived': entries_table.c.is_archived
        }
    )
    mapper.map_imperatively(
        InventoryEntry,
        inventory_entries_table,
    )