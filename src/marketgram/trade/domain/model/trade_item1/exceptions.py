class DomainError(Exception):
    pass


class InvalidOperationError(Exception):
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