from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Deadlines:
    shipment: datetime | None
    receipt: datetime | None
    inspection: datetime
    shipped_to: datetime | None = None
    received_in: datetime | None = None
    inspected_in: datetime | None = None

    def shipped(self, occurred_at: datetime) -> 'Deadlines':
        return Deadlines(
            self.shipment,
            self.receipt,
            self.inspection,
            occurred_at
        )
    
    def received(self, occurred_at: datetime) -> 'Deadlines':
        return Deadlines(
            self.shipment,
            self.receipt,
            self.inspection,
            self.shipped_to,
            occurred_at
        )
    
    def inspected(self, occurred_at: datetime) -> 'Deadlines':
        return Deadlines(
            self.shipment,
            self.receipt,
            self.inspection,
            self.shipped_to,
            self.received_in,
            self.received_in,
            occurred_at
        )