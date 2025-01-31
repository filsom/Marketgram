from dataclasses import dataclass
from datetime import datetime

from marketgram.trade.domain.model.p2p.status_deal import StatusDeal


@dataclass(frozen=True)
class Deadlines:
    shipment: datetime
    inspection: datetime
    
    def check(
        self, 
        status: StatusDeal,
        occurred_at: datetime
    ) -> bool:
        match status:
            case StatusDeal.NOT_SHIPPED:
                return occurred_at < self.shipment
            
            case StatusDeal.INSPECTION:
                return occurred_at < self.inspection