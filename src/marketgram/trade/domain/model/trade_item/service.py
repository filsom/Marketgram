from decimal import Decimal
from uuid import uuid4

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.p2p.status_deal import StatusDeal
from marketgram.trade.domain.model.p2p.type_deal import TypeDeal
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.category import Category
from marketgram.trade.domain.model.trade_item.type_category import TypeCategory


class Service:
    def __init__(
        self,
        name: str,
        alias: str,
        categories: list[Category],
        service_id: int = None,
    ) -> None:
        self._service_id = service_id
        self._name = name
        self._alias = alias
        self._categories = categories

    def create_new_category(
        self,
        category_types: TypeCategory,
        status_deal: StatusDeal,
        type_deal: TypeDeal,
        action_time: ActionTime,
        min_price: Money,
        min_procent_discount: Decimal,
    ) -> Category:
        if min_price <= Money(0):
            raise DomainError()
        
        if 0 >= min_procent_discount >= 1:
            raise DomainError()

        if self._categories:
            for category in self._categories:
                if category_types.type_category_id == category.category_type_id:
                    raise DomainError()
                
        salt = str(uuid4()).split('-')[-1]
        category_alias = '{}-{}'.format(category_types.name, salt)
        
        return Category(
            self._service_id,
            category_types.type_category_id,
            category_alias,
            action_time,
            type_deal,
            status_deal,
            min_price,
            min_procent_discount
        )
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def service_id(self) -> int:
        return self._service_id
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Service):
            return False

        return self.service_id == other.service_id
    
    def __hash__(self) -> int:
        return hash(self.service_id)