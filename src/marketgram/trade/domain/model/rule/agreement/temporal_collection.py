from datetime import date

from marketgram.trade.domain.model.rule.agreement.limits import (
    Limits
)


class TemporalCollection:
    def __init__(self):
        self._contents = {}
        self._cache: list[date] = None

    def get(self, date: date):
        for milestone in self._milestone():
            if milestone <= date:
                return self._contents.get(milestone)
            
        raise ValueError

    def put(self, date_from: date, limit: Limits):
        self._contents[date_from] = limit
        self._cache = None

    def _milestone(self):
        if self._cache is None:
            self._calculate_milestones()
        
        return self._cache

    def _calculate_milestones(self):
        self._cache = list(self._contents.keys())
        self._cache.sort()
        self._cache.reverse()