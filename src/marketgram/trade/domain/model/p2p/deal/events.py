from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DisputeOpenedEvent:
    seller_id: UUID
    occurred_at: datetime


@dataclass(frozen=True)
class DisputeClosedEvent:
    seller_id: UUID
    occurred_at: datetime