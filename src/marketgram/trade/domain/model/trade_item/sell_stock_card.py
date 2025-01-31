from datetime import datetime
from uuid import UUID

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.events import PurchasedCardWithAutoShipmentEvent
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal
from marketgram.trade.domain.model.p2p.members import Members
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.trade_item.sell_card import SellCard
from marketgram.trade.domain.model.trade_item.status_card import StatusCard


class SellStockCard(SellCard):
    def purchase(
        self, 
        buyer_id: UUID, 
        quantity: int, 
        occurred_at: datetime
    ) -> ShipDeal:
        # Добавить работу с товарными остатками!
        if quantity <= 0:
            raise DomainError()
        
        deal = ShipDeal(
            self._card_id,
            Members(self._owner_id, buyer_id),
            quantity,
            self._shipment,
            self._price * quantity,
            self._action_time.create_deadlines(occurred_at),
            StatusDeal.NOT_SHIPPED,
            occurred_at
        )  
        self._status = StatusCard.PURCHASED
        self.events.append(
            PurchasedCardWithAutoShipmentEvent(deal, occurred_at)
        )
        return deal