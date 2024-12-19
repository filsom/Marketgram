from typing import Protocol
from uuid import UUID

from marketgram.trade.domain.model.p2p.seller import Seller
from marketgram.trade.domain.model.p2p.user import User


class MembersRepository(Protocol):
    def add(self, seller: Seller) -> None:
        raise NotImplementedError
    
    def next_identity(self) -> UUID:
        raise NotImplementedError
    
    async def seller_with_id(self, user_id: UUID) -> Seller | None:
        raise NotImplementedError
    
    async def seller_with_balance_and_id(self, user_id: UUID) -> Seller | None:
        raise NotImplementedError
    
    async def user_with_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError
    
    async def user_with_balance_and_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError