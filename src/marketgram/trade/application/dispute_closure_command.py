from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum, auto
from uuid import UUID

from marketgram.common.application.id_provider import IdProvider
from marketgram.trade.application.exceptions import ApplicationError
from marketgram.trade.domain.model.p2p.deal_repository import DealsRepository


class Solution(StrEnum):
    BUYER = auto()
    SELLER = auto()


@dataclass
class DisputeClosureCommand:
    deal_id: int
    solution: Solution


class DisputeClosureHandler:
    def __init__(
        self,
        id_provider: IdProvider,
        deals_repository: DealsRepository
    ) -> None:  
        self._id_provider = id_provider
        self._deals_repository = deals_repository

    async def handle(self, command: DisputeClosureCommand) -> None:
        deal = await self._deals_repository \
            .disputed_with_id(command.deal_id)
        
        if deal is None:
            raise ApplicationError()
        
        current_time = datetime.now(UTC)
        match command.solution:
            case Solution.BUYER:
                deal.satisfy_buyer(current_time)

            case Solution.SELLER:
                deal.satisfy_seller(current_time)