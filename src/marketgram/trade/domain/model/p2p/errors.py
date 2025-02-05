from marketgram.common.domain.model.errors import DomainError


class AddLinkError(DomainError):
    pass


AUTO_LINK = 'Не требуется добавление ссылки!'
IN_THE_CHAT = 'Отгрузка товара производится в переписке.'
RE_ADD = 'Повторное добавление!'
MISSING_DOWNLOAD_LINK = 'Отсутствует ссылка для скачивания!'


class CheckDeadlineError(DomainError):
    pass


OVERDUE_SHIPMENT = 'Отгрузка товара просрочена! Будет осуществлен автоматический возврат денежных средств покупателю!'
RETURN_TO_BUYER = 'Будет осуществлен автоматический возврат денежных средств покупателю!'
PAYMENT_TO_SELLER = 'Ожидайте, покупатель не подтвердил получение, деньги автоматически поступят на ваш баланс.'
LATE_CONFIRMATION = 'Ожидайте, деньги за товар автоматически поступят на баланс продавца!'
DO_NOT_OPEN_DISPUTE = 'Спор не отркыть! Привышено время.'


class QuantityItemError(DomainError):
    pass


class OpenedDisputeError(DomainError):
    pass
