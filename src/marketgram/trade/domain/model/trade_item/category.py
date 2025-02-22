from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from marketgram.common.errors import DomainError
from marketgram.trade.domain.model.money import Money
from marketgram.trade.domain.model.p2p.shipment import Shipment
from marketgram.trade.domain.model.statuses import StatusCard
from marketgram.trade.domain.model.trade_item.action_time import ActionTime
from marketgram.trade.domain.model.trade_item.card import ModerationCard


class Category:
    def __init__(
        self,
        name: str,
        alias: str,
        path: str | None,
        type_category_id: int,
        action_time: ActionTime | None = None,
        shipment: Shipment | None = None,
        minimum_unit_price: Money | None = None,
        minimum_procent_discount: Decimal | None = None,
        category_id: int | None = None,
        subcategories: list[int] | None = None
    ) -> None:
        self._category_id = category_id
        self._name = name
        self._alias = alias
        self._path = path
        self._type_category_id = type_category_id
        self._action_time = action_time
        self._shipment = shipment
        self._minimum_unit_price = minimum_unit_price
        self._minimum_procent_discount = minimum_procent_discount
        self._subcategories = subcategories

    def make_card(
        self,
        user_id: int,
        name: str,
        body: str,
        unit_price: Money,
        features: dict[str, str], 
        action_time: dict[str, int] | None,
        current_date: datetime
    ) -> ModerationCard:
        nesting = self._path.split('/')
        if len(nesting) == 1:
            raise DomainError()
        
        if unit_price < self._minimum_unit_price: 
            raise DomainError()
        
        if action_time is None:  
            action_time = self._action_time
        
        card = ModerationCard(
            user_id,
            self._category_id,
            unit_price,
            unit_price,
            name,
            body,
            features,
            action_time,
            self._shipment,
            current_date,
            StatusCard.ON_FIRST_MODERATION
        )
        return card

    def create_subcategory(
        self, 
        name: str, 
        type_category_id: int,
        shipment: Shipment,
        action_time: ActionTime,
        minimum_unit_price: Money,
        minimum_procent_discount: Decimal
    ) -> "Category":
        if minimum_unit_price <= Money(0):
            raise DomainError()
        
        if 0 >= minimum_procent_discount >= 1:
            raise DomainError()

        if shipment.is_auto_link():
            raise DomainError()
        
        alias = Category.make_alias(name)
        path = "{}/{}".format(path, alias)
    
        if self._subcategories:
            for sub in self._subcategories:
                if sub.type_category_id == type_category_id:
                    raise DomainError()
        else:
            self._path = path

        subcategory = Category(
            name,
            alias,
            path,
            type_category_id,
            action_time,
            shipment,
            minimum_unit_price,
            minimum_procent_discount
        )  
        return subcategory

    @staticmethod
    def create_basic(
        name: str, 
        type_category_id: int, 
    ) -> "Category":
        return Category(
            name.lower(),
            Category.make_alias(name),
            None,
            type_category_id
        )
    
    @staticmethod
    def make_alias(name: str) -> str:
        salt = str(uuid4()).split()[-1]
        alias = "{}-{}".format(name.lower(), salt)
        return alias
    
    @property
    def type_category_id(self) -> int:
        return self._type_category_id
    
    @property
    def path(self) -> str:
        return self._path
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return False

        return self._category_id == other._category_id
    
    def __hash__(self) -> int:
        return hash(self._category_id)