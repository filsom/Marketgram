from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item1.card import Card
from marketgram.trade.domain.model.trade_item1.category1 import Path
from marketgram.trade.domain.model.trade_item1.description import Description


@dataclass
class TypeCategory:
    title: str
    type_category_id: int = None

    def __post_init__(self) -> None:
        if not len(self.title):
            raise DomainError()
        
        self.title = self.title.lower()


class Category:
    def __init__(
        self,
        title: str,
        alias: str,
        path: Path,
        min_price: Money,
        min_procent_discount: Decimal,
        category_id: int = None
    ) -> None:
        self._category_id = category_id
        self._title = title
        self._alias = alias
        self._path = path
        self._min_price = min_price
        self._min_procent_discount = min_procent_discount
    
    def make_card(
        self,
        owner_id: UUID,
        price: Money, 
        description: Description,
        current_time: datetime,
    ) -> Card:
        raise NotImplementedError()
        
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def alias(self) -> str:
        return self._alias
    
    @property
    def path(self) -> Path:
        return self._path


class TelegramAccoutsTdataSJCategory(Category):
    def make_card(
        self,
        owner_id: UUID,
        price: Money, 
        description: Description,
        current_time: datetime,
    ) -> Card:
        if price < self._min_price:
            raise DomainError()