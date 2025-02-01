from marketgram.common.domain.model.errors import DomainError


class AddLinkError(DomainError):
    pass


AUTO_LINK = 'Не требуется добавление ссылки!'
IN_THE_CHAT = 'Отгрузка товара производится в переписке.'
RE_ADD = 'Повторное добавление!'
MISSING_DOWNLOAD_LINK = 'Отсутствует ссылка для скачивания!'


class CheckDeadlineError(DomainError):
    pass


OVERDUE_SHIPMENT = 'Отгрузка товара просрочена!'