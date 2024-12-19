from enum import StrEnum, auto


class TransferMethod(StrEnum):
    AUTO_PROVIDE = auto()
    PROVIDES_SELLER = auto()

    def is_auto(self) -> bool:
        return self in TransferMethod.AUTO_PROVIDE
    
    def is_provides_seller(self) -> bool:
        return self in TransferMethod.PROVIDES_SELLER