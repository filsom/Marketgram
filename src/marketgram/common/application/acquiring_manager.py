from typing import Protocol

from marketgram.trade.domain.model.p2p.payment import Payment


class AcquiringManager(Protocol):
    def take_payment(self, payment: Payment):
        raise NotImplementedError