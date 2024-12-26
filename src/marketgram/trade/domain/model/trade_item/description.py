from dataclasses import dataclass
from enum import StrEnum, auto


class AccountFormat(StrEnum):
    Autoreg = auto()


class Region(StrEnum):
    Random = auto()
    Sng = auto()
    Europe = auto()
    Asia = auto()
    America = auto()
    Other = auto()


@dataclass
class Description:
    title: str
    text_description: str
    account_format: AccountFormat
    region: Region
    spam_block: bool