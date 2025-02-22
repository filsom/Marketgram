from marketgram.trade.domain.model.p2p.deal.opened_dispute import OpenedDispute


class DisputesRepository:
    async def add(self, dispute: OpenedDispute) -> None:
        pass