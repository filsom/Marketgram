from enum import StrEnum, auto


class TransferFormat(StrEnum):
    LOGIN_CODE = auto()
    LINK = auto()

    def is_code(self) -> bool:
        return self in TransferFormat.LOGIN_CODE
    
    def is_link(self) -> bool:
        return self in TransferFormat.LINK