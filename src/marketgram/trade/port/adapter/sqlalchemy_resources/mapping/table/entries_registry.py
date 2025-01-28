from sqlalchemy.orm import registry, composite

from marketgram.trade.domain.model.entry import PostingEntry
from marketgram.trade.domain.model.money import Money
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.entries_table import (
    entries_table
)


def entries_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        PostingEntry,
        entries_table,
        properties={
            '_user_id': entries_table.c.user_id,
            '_amount': composite(Money, entries_table.c.amount),
            '_account_type': entries_table.c.account_type,
            '_operation': entries_table.c.operation,
            '_posted_in': entries_table.c.posted_in,
            '_entry_status': entries_table.c.entry_status,
            '_is_archived': entries_table.c.is_archived
        }
    )