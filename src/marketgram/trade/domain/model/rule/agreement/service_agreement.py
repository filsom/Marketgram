from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from marketgram.trade.domain.model.trade_item.exceptions import (
    NO_RULE, 
    DomainError
)
from marketgram.trade.domain.model.p2p.deadlines import Deadlines
from marketgram.trade.domain.model.rule.agreement.limits import (
    Limits
)
from marketgram.trade.domain.model.rule.agreement.posting_rule import PostingRule
from marketgram.trade.domain.model.rule.agreement.temporal_collection import (
    TemporalCollection
)
from marketgram.trade.domain.model.rule.agreement.types import EventType

if TYPE_CHECKING:
    from marketgram.trade.domain.model.rule.agreement.payout_rule import PayoutPostingRule
    from marketgram.trade.domain.model.rule.agreement.deal_rule import DealPostingRule


class ServiceAgreement:
    def __init__(self, default_deadlines: Deadlines):
        self._deadlines = default_deadlines
        self._new_limits: list[Limits] = []
        self._past_limits = TemporalCollection()
        self._posting_rules: dict[
            EventType, PostingRule
        ] = {}

    def new_limits(self, limits: Limits) -> None:
        self._new_limits.append(limits)
        self._add_limits(limits)

    def limits_from(self, date: datetime) -> Limits:
        return self._past_limits.get(date.date())

    def actual_limits(self) -> Limits:
        current_date = datetime.now()
        return self._past_limits.get(current_date.date())

    def default_deadlines(self) -> Deadlines:
        return self._deadlines

    def add_rule(self, event_type: EventType, rule: PostingRule) -> None:
        self._posting_rules[event_type] = rule

    def find_payout_rule(self, event_type: EventType) -> PayoutPostingRule:
        return self._find_rule(event_type)
    
    def find_deal_rule(self, event_type: EventType) -> DealPostingRule:
        return self._find_rule(event_type)

    def _find_rule(self, event_type: EventType) -> PostingRule:
        rule = self._posting_rules.get(event_type, None)
        if rule is None:
            raise DomainError(NO_RULE)
        
        return rule
    
    def _add_limits(self, limits: Limits) -> None:
        self._past_limits.put(limits.install_date.date(), limits)