from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.common.entity import IntegrationEvent
from marketgram.trade.domain.model.statuses import StatusCard


@dataclass(frozen=True)
class DisputeOpenedNotification(IntegrationEvent):
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class DealCreatedNotification(IntegrationEvent):
    seller_id: int
    deal_id: int
    card_id: int
    qty: int
    shipped_at: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedByDealNotification(IntegrationEvent):
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedReplacementByDisputeNotification(IntegrationEvent):
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ZeroInventoryBalanceNotification(IntegrationEvent):
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerCancelledDealNotification(IntegrationEvent):
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ReissuePurchasedCardNotification(IntegrationEvent):
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class AdminJoinNotification(IntegrationEvent):
    deal_id: int
    occurred_at: datetime


# Пользователь отклонил возврат товара (некачесвенный). Ждем админа!
@dataclass(frozen=True)
class BuyerRejectedReplacementNotification(IntegrationEvent):
    deal_id: int
    dispute_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class InventoryBalancesAddedNotification(IntegrationEvent):
    card_id: int
    owner_id: UUID
    qty: int
    status_card: StatusCard
    occurred_at: datetime


@dataclass(frozen=True)
class AdminRejectedModerationCardNotification(IntegrationEvent):
    card_id: int
    status_card: StatusCard
    reason: str
    occurred_at: datetime