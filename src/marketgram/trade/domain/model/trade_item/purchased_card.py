from marketgram.trade.domain.model.statuses import StatusCard


class PurchasedCard:
    def __init__(
        self,
        card_id: int,
        status: StatusCard
    ) -> None:
        self._card_id = card_id
        self._status = status

    def reissue(self) -> None:
        self._status = StatusCard.ON_SALE
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PurchasedCard):
            return False

        return self._card_id == other._card_id
    
    def __hash__(self) -> int:
        return hash(self._card_id)