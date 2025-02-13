from dataclasses import dataclass
from datetime import datetime, timedelta

from marketgram.common.errors import DomainError
from marketgram.trade.domain.model.p2p.deal.deadlines import Deadlines


@dataclass(frozen=True)
class ActionTime:
    shipping_hours: int
    inspection_hours: int

    def __post_init__(self) -> None:
        if self.shipping_hours < 1:
            raise DomainError()
        
        if self.inspection_hours < 1:
            raise DomainError()
        
    def create_deadlines(self, current_time: datetime) -> Deadlines:
        ship_to = current_time + timedelta(hours=self.shipping_hours)
        inspect_to = ship_to + timedelta(hours=self.inspection_hours)

        return Deadlines(ship_to, inspect_to)