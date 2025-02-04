from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.deal.unconfirmed_deal import Claim
from marketgram.trade.domain.model.p2p.members import DisputeMembers


class Dispute:
    def __init__(
        self,
        dispute_id: UUID,
        claim: Claim,
        dispute_members: DisputeMembers,
        price: Money,
        open_in: datetime,
    ) -> None:
        self._dispute_id = dispute_id
        self._claim = claim
        self._dispute_members = dispute_members
        self._price = price
        self._open_in = open_in