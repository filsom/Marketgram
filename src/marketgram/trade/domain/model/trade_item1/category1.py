from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4

from marketgram.common.application.exceptions import DomainError
from marketgram.trade.domain.model.trade_item1.card import Card


ACCOUNTS = 'Аккаунты'


@dataclass
class Path:
    value: str

    def __post_init__(self) -> None:
        self.value = '/{}/'.format(self.value.lower())

    def nesting(self) -> int:
        return len(list(filter(None, self.value.split('/'))))
    
    def expand(self, value: str) -> Path:
        return Path('{}/{}'.format(self.value.strip('/'), value.lower()))
    

class Сategory:
    def __init__(
        self,
        parent_id: int,
        title: str,
        alias: str,
        path: Path,
        min_price,
        min_procent_discount,
        subcategories: list[Сategory],
        subcategory_id: int = None,
    ) -> None:
        self._subcategory_id = subcategory_id
        self._parent_id = parent_id
        self._title = title
        self._alias = alias
        self._path = path
        self._subcategories = subcategories

    def make_card(self) -> Card:
        raise NotImplementedError

    @property
    def title(self) -> str:
        return self._title


class TelegramTdataSessionJson(Сategory):
    pass


class TelegramLoginCode(Сategory):
    pass


class Category:
    def __init__(
        self,
        title: str,
        alias: str,
        path: Path,
        subcategories: list[Сategory],
        category_id: int = None,
    ) -> None:
        self._category_id = category_id
        self._title = title
        self._alias = alias
        self._path = path
        self._subcategories = subcategories

    def add_subcategory(self, title: str, alias: str) -> None:
        for subcategory in self._subcategories:
            if subcategory.title == title:
                raise DomainError()
            
        alias = '{}-{}'.format(alias, str(uuid4()).split('-')[-1])

        self._subcategories.append(
            Сategory(
                self._category_id, 
                title, 
                alias, 
                self._path.expand(alias), 
                []
            )
        )

    def make_card(self, title_category: str):
        for subcategory in self._subcategories:
            if subcategory == title_category:
                return subcategory.make_card()