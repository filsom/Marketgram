from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from marketgram.trade.domain.model.entry_status import EntryStatus
from marketgram.trade.domain.model.events import DisputeClosedEvent
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.shipment import Shipment
from marketgram.trade.domain.model.p2p.deal.unconfirmed_deal import Claim
from marketgram.trade.domain.model.p2p.errors import QuantityItemError
from marketgram.trade.domain.model.p2p.members import DisputeMembers
from marketgram.trade.domain.model.p2p.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.posting_entry import PostingEntry
from marketgram.trade.domain.model.types import AccountType, Operation


class StatusDispute(StrEnum):
    OPEN = auto()
    ADMIN_JOINED = auto()
    CLOSED = auto()


class Dispute:
    def __init__(
        self,
        dispute_id: UUID,
        claim: Claim,
        dispute_members: DisputeMembers,
        unit_price: Money,
        qty_purchased: int,
        shipment: Shipment,
        open_in: datetime,
        status: StatusDispute,
    ) -> None:
        self._dispute_id = dispute_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._unit_price = unit_price
        self._qty_purchased = qty_purchased
        self._shipment = shipment
        self._open_in = open_in
        self._status = status

    def satisfy_buyer(self, qty_return: int, occurred_at: datetime) -> None:
        if self._claim.qty_return != qty_return:
            raise QuantityItemError()
        
        if self._claim.return_is_money():
            pass

    def satisfy_seller(self, occurred_at: datetime) -> None:
        pass