from enum import StrEnum, auto


class Format(StrEnum):
    LOGIN_CODE = auto()
    LINK = auto()

    def is_code(self) -> bool:
        return self in Format.LOGIN_CODE
    
    def is_link(self) -> bool:
        return self in Format.LINK