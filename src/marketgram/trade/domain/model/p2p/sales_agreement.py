from dataclasses import dataclass

from marketgram.trade.domain.model.p2p.format import TransferFormat
from marketgram.trade.domain.model.p2p.transfer_method import TransferMethod
from marketgram.trade.domain.model.trade_item.exceptions import DomainError


@dataclass(frozen=True)
class StepTime:
    shipping_hours: int | None
    receipt_hours: int | None
    inspection_hours: int

    def __post_init__(self) -> None:
        for key in self.__dict__:
            if self.__dict__[key] is not None and self.__dict__[key] < 1:
                raise DomainError()


@dataclass(frozen=True)
class SalesAgreement:
    transfer_format: TransferFormat
    transfer_method: TransferMethod
    shipping_hours: int | None
    receipt_hours: int | None
    inspection_hours: int

    def __post_init__(self) -> None:
        if self.shipping_hours is not None and self.shipping_hours < 1:
            raise DomainError()

    def is_auto_link(self) -> bool:
        return self.transfer_method.is_auto() and self.transfer_format.is_link()
    
    def is_providing_link(self) -> bool:
        return self.transfer_method.is_provides_seller() and self.transfer_format.is_link()
    
    def is_providing_code(self) -> bool:
        return self.transfer_method.is_provides_seller() and self.transfer_format.is_code()