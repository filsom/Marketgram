from __future__ import annotations
from decimal import Decimal

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.rule.agreement.money import Money


class Category:
    def __init__(
        self,
        name: str,
        alias: str,
        subcategory: list[Category], 
        category_id: int = None,
        parent_category_id: int = None,
        category_type_id: int = None,
        minimum_price: Money = None,
        minimum_procent_discount: Decimal = None
    ) -> None:
        self._name = name
        self._alias = alias
        self._subcategory = subcategory
        self._category_id = category_id
        self._parent_category_id = parent_category_id
        self._category_type_id = category_type_id
        self._minimum_price = minimum_price
        self._minimum_procent_discount = minimum_procent_discount

    def add_subcategory(
        self,
        name: str,
        category_type_id: int,
        minimum_price: Money,
        minimum_procent_discount: Decimal
    ) -> None:
        if self._parent_category_id:
            raise DomainError()

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