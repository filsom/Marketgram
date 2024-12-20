from dataclasses import dataclass
from uuid import UUID

from marketgram.trade.domain.model.p2p.members_repository import (
    MembersRepository
)
from marketgram.trade.domain.model.p2p.user import User


@dataclass
class MemberCreatedEvent:
    member_id: UUID


class MemberCreatedEventHandler:
    def __init__(
        self,
        members_repository: MembersRepository
    ) -> None:
        self._members_repository = members_repository

    async def handle(self, event: MemberCreatedEvent) -> None:
        member = await self._members_repository \
            .user_with_id(event.member_id)
        
        if member is None:
            new_member = User(event.member_id)

            return self._members_repository.add(new_member)