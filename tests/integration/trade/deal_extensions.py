from typing import Self

from marketgram.trade.domain.model.p2p.deal.cancellation_deal import CancellationDeal
from marketgram.trade.domain.model.p2p.deal.confirmation_deal import ConfirmationDeal
from marketgram.trade.domain.model.p2p.deal.dispute_deal import DisputeDeal
from marketgram.trade.domain.model.p2p.deal.ship_deal import ShipDeal


class DealExtensions:
    def __init__(
        self,
        unshipped: ShipDeal | None,
        unconfirmed: ConfirmationDeal | None,
        unclosed: CancellationDeal | None,
        not_disputed: DisputeDeal | None,
        disputed: DisputeDeal | None,
    ) -> None:
        self._unshipped = unshipped
        self._unconfirmed = unconfirmed
        self._unclosed = unclosed
        self._not_disputed = not_disputed
        self._disputed = disputed

    def can_be_shipped(self) -> Self:
        assert self._unshipped is not None
        return self

    def cannot_shipped(self) -> Self:
        assert self._unshipped is None
        return self
    
    def can_be_сonfirmed(self) -> Self:
        assert self._unconfirmed is not None
        return self
    
    def cannot_be_confirmed(self) -> Self:
        assert self._unconfirmed is None
        return self
    
    def can_be_closed(self) -> Self:
        assert self._unclosed is not None
        return self
    
    def cannot_be_closed(self) -> Self:
        assert self._unclosed is None
        return self
    
    def can_open_dispute(self) -> Self:
        assert self._not_disputed is not None
        return self
    
    def cannot_open_duspute(self) -> Self:
        assert self._not_disputed is None
        return self
    
    def dispute_was_opened(self) -> Self:
        assert self._disputed is not None
        return self
    
    def there_was_no_dispute(self) -> Self:
        assert self._disputed is None
        return self