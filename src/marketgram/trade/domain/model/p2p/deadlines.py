from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Deadlines:
    shipment: datetime
    receipt: datetime
    inspection: datetime