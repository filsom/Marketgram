from marketgram.common.application.exceptions import DomainError


class PersonalDataError(DomainError):
    pass


INVALID_EMAIL_OR_PASSWORD = 'Неверный Email или пароль!'