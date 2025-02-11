from marketgram.common.errors import DomainError


class PersonalDataError(DomainError):
    pass


INVALID_EMAIL_OR_PASSWORD = 'Неверный Email или пароль!'