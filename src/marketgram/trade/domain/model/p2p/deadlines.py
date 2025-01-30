from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Deadlines:
    shipment: datetime
    inspection: datetime

    def check_shipment(self, occurred_at: datetime) -> bool:
        return occurred_at < self.shipment
    
    def check_inspection(self, occurred_at: datetime) -> bool:
        return occurred_at < self.inspection