from dataclasses import asdict, dataclass
from enum import StrEnum, auto


class RegistrationMethod(StrEnum):
    Autoreg = auto()
    Hand = auto()


class AccountFormat(StrEnum):
    Tdata = auto()
    Tdata_and_session_json = auto()
    Session_json = auto()
    Code = auto()


class Region(StrEnum):
    Random = auto()
    Sng = auto()
    Europe = auto()
    Asia = auto()
    America = auto()
    Other = auto()


# @dataclass
# class Description:
#     title: str
#     text_description: str
#     account_format: RegistrationMethod
#     region: Region
#     spam_block: bool


class RegistrationMethod(StrEnum):
    Autoreg = auto()
    Hand = auto()


class AccountFormat(StrEnum):
    Tdata = auto()
    Tdata_and_session_json = auto()
    Session_json = auto()
    Code = auto()


class Region(StrEnum):
    Random = auto()
    Sng = auto()
    Europe = auto()
    Asia = auto()
    America = auto()
    Other = auto()
    

@dataclass
class Characteristics:
    pass


@dataclass
class TelegramAccCharacteristics(Characteristics):
    region: Region
    account_format: AccountFormat
    registration_method: RegistrationMethod | None = None
    avatar: bool | None = None
    two_fa: bool | None = None
    premium_activated: bool | None = None
    spam_block: bool | None = None


class TelegramAcc:
    pass


@dataclass
class Description:
    title: str
    body: str
    characteristics: Characteristics
    transfer_format: str
    
    def __post_init__(self) -> None:
        self.characteristics = asdict(self.characteristics)