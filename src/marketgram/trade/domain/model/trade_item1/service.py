from decimal import Decimal
from uuid import uuid4

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.rule.agreement.money import Money
from marketgram.trade.domain.model.trade_item1.category import (
    Category, 
    TypeCategory
)
from marketgram.trade.domain.model.trade_item1.category1 import Path


class Service:
    def __init__(
        self,
        title: str,
        alias: str,
        categories: list[Category],
    ) -> None:
        self._title = title
        self._alias = alias
        self._categories = categories

    def create_new_category(
        self,
        min_price: Money,
        min_procent_discount: Decimal,
        category_types: TypeCategory
    ) -> Category:
        if min_price <= Money(0):
            raise DomainError()
        
        if 0 >= min_procent_discount >= 1:
            raise DomainError()

        new_category_title = '{}.{}'.format(
            self._title, category_types.title
        )
        if self._categories:
            for category in self._categories:
                if category._title == new_category_title:
                    raise DomainError()
                
        salt = str(uuid4()).split('-')[-1]
        category_alias = '{}-{}'.format(category_types.title, salt)
        category_path = Path(self._alias).expand(category_alias)
        
        return Category(
            new_category_title,
            category_alias,
            category_path,
            min_price,
            min_procent_discount
        )