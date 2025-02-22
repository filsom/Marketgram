from dataclasses import dataclass
from datetime import datetime

from marketgram.trade.domain.model.statuses import StatusDeal


@dataclass(frozen=True)
class Deadlines:
    ship_to: datetime
    inspect_to: datetime
    
    def check(self, status: StatusDeal, occurred_at: datetime) -> bool:
        match status:
            case StatusDeal.NOT_SHIPPED:
                return occurred_at < self.ship_to
            
            case StatusDeal.INSPECTION:
                return occurred_at < self.inspect_to