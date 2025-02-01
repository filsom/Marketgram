from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto


class InventoryOperation(StrEnum):
    UPLOADING = auto()
    BUY = auto()


@dataclass
class InventoryEntry:
    qty: int
    posted_in: datetime
    operation: InventoryOperation