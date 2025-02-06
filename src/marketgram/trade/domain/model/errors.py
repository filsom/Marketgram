from marketgram.common.domain.model.errors import DomainError


class CheckDeadlineError(DomainError):
    pass


class AddLinkError(DomainError):
    pass

MISSING_DOWNLOAD_LINK = 'Отсутствует ссылка для скачивания!'
OVERDUE_SHIPMENT = 'Отгрузка товара просрочена! Будет осуществлен автоматический возврат денежных средств покупателю!'
RETURN_TO_BUYER = 'Будет осуществлен автоматический возврат денежных средств покупателю!'
PAYMENT_TO_SELLER = 'Ожидайте, покупатель не подтвердил получение, деньги автоматически поступят на ваш баланс.'
LATE_CONFIRMATION = 'Ожидайте, деньги за товар автоматически поступят на баланс продавца!'
DO_NOT_OPEN_DISPUTE = 'Спор не отркыть! Привышено время.'


class QuantityItemError(DomainError):
    pass


class OpenedDisputeError(DomainError):
    pass


BUY_FROM_YOURSELF = 'Нельзя купить свой товар!'
MINIMUM_PRICE = 'Цена товара меньше минимальной!'
MINIMUM_DEPOSIT = 'Сумма меньше минимальной'
MINIMUM_WITHDRAW = 'Сумма вывода меньше минимальной!'
DISCOUNT_ERROR = 'Невозможно установить скидку!'
INCORRECT_VALUES = 'Задан некорректный лимит {}!'
UNACCEPTABLE_DISCOUNT_RANGE = (
        'Некорректная скидочная цена! Цена с учетом скидки должна быть в диапозоне {} до {} RUB'
)
BALANCE_BLOCKED = 'Операции с балансом невозможны. Ваш баланс заблокирован!'
BALANCE_IS_FROZEN = 'Баланс заморожен для вывода средств!'
INSUFFICIENT_FUNDS = 'Недостаточно средств'
NO_RULE = 'Невозможно выполнить операцию! Правило публикации отсутствует.'
NO_WITHDRAWAL = 'Заявка на вывод средств отсутствует!'


class ReplacingItemError(DomainError):
    pass
