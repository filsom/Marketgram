from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.statuses import StatusCard


@dataclass(frozen=True)
class DisputeOpenedNotification:
    seller_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class DealCreatedNotification:
    seller_id: int
    deal_id: int
    card_id: int
    qty: int
    shipped_at: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedByDealNotification:
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ShippedReplacementByDisputeNotification:
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ZeroInventoryBalanceNotification:
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class SellerCancelledDealNotification:
    buyer_id: int
    deal_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class ReissuePurchasedCardNotification:
    seller_id: int
    card_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class AdminJoinNotification:
    deal_id: int
    occurred_at: datetime


# Пользователь отклонил возврат товара (некачесвенный). Ждем админа!
@dataclass(frozen=True)
class BuyerRejectedReplacementNotification:
    deal_id: int
    dispute_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class InventoryBalancesAddedNotification:
    card_id: int
    owner_id: UUID
    qty: int
    status_card: StatusCard
    occurred_at: datetime