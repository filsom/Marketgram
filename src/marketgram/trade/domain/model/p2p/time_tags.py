from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TimeTags:
    created_at: datetime
    shipped_at: datetime | None = field(default=None)
    received_at: datetime | None = field(default=None)
    closed_at: datetime | None = field(default=None)

    def shipped(self, current_date: datetime) -> TimeTags:
        return TimeTags(
            self.created_at,
            current_date
        )

    def received(self, current_date: datetime) -> TimeTags:
        return TimeTags(
            self.created_at,
            self.shipped_at,
            current_date
        )

    def closed(self, current_date: datetime) -> TimeTags:
        return TimeTags(
            self.created_at,
            self.shipped_at,
            self.received_at,
            current_date
        )

    def closing_reset(self) -> TimeTags:
        return TimeTags(
            self.created_at,
            self.shipped_at,
            self.received_at
        )