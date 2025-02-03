from sqlalchemy.orm import registry

from marketgram.trade.domain.model.trade_item.inventory_entry import InventoryEntry
from marketgram.trade.port.adapter.sqlalchemy_resources.mapping.table.inventory_entries_table import (
    inventory_entries_table
)


def inventory_entries_registry_mapper(mapper: registry) -> None:
    mapper.map_imperatively(
        InventoryEntry,
        inventory_entries_table,
    )