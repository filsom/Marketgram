from datetime import datetime
from uuid import UUID

from marketgram.trade.domain.model.exceptions import DomainError
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.time_tags import TimeTags
from marketgram.trade.domain.model.rule.agreement.entry import PostingEntry
from marketgram.trade.domain.model.rule.agreement.service_agreement import ServiceAgreement
from marketgram.trade.domain.model.rule.agreement.types import EventType


class ConfirmationDeal:
    def __init__(
        self, 
        deal_id: UUID,
        card_created_at: datetime,
        time_tags: TimeTags,
        deadlines: Deadlines,
        status: StatusDeal,
        entries: list[PostingEntry]
    ) -> None:
        self._deal_id = deal_id
        self._card_created_at = card_created_at
        self._time_tags = time_tags
        self._deadlines = deadlines
        self._status = status
        self._entries = entries
        self._agreement: ServiceAgreement = None

    def confirm_quality(self, occurred_at: datetime) -> None:
        if self.check_deadline() < occurred_at:
            raise DomainError()
        
        limits = self._agreement.limits_from(   
            self._card_created_at
        )
        rule = self._agreement.find_deal_rule(
            EventType.PRODUCT_CONFIRMED
        )
        rule.process(self, limits)

        self._time_tags.closed(occurred_at)
        self._status = StatusDeal.CLOSED

    def check_deadline(self) -> datetime:
        return (self._time_tags.received_at 
                + self._deadlines.total_check_hours)
    
    def transferred_agreement(self) -> ServiceAgreement:
        return self._agreement

    def accept_agreement(self, agreement: ServiceAgreement) -> None:
        self._agreement = agreement

    def __repr__(self) -> str:
        return (
            f'ConfirmationDeal('
                f'deal_id={self._deal_id}, '
                f'card_created_at={self._card_created_at}, '
                f'time_tags={self._time_tags}, '
                f'deadlines={self._deadlines}, ' 
                f'status={self._status}, '
                f'entries={self._entries}, '
                f'agreement={self._agreement}'
            ')'
        )
    
    def __eq__(self, other: 'ConfirmationDeal') -> bool:
        if not isinstance(other, ConfirmationDeal):
            return False

        return self._deal_id == other._deal_id
    
    def __hash__(self) -> int:
        return hash(self._deal_id)