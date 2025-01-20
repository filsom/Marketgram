from enum import StrEnum, auto


class TransferMethod(StrEnum):
    AUTO = auto()
    SELLER = auto()

    def is_auto(self) -> bool:
        return self in TransferMethod.AUTO
    
    def is_provides_seller(self) -> bool:
        return self in TransferMethod.SELLER