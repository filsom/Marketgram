class InfrastructureError(Exception):
    pass


class AnalysisErrorHMAC(InfrastructureError):
    pass

UNKNOWN_VALUE = 'Неизвестное значение'


class AuthorisationError(InfrastructureError):
    pass

ACCESS_DENIED = 'Требуется авторизация. Пожалуйста, войдите в свою учетную запись!'


class  JwtVerifyError(InfrastructureError):
    pass

JWT_ERROR = 'Некорректный токен'


class UnknowError(Exception):
    pass

UNKNOWN_EXCEPTION = 'Возникла неизвестная ошибка. Повторите операцию позже!'


class AuthProviderError(Exception):
    pass


INVALID_CREDENTIALS = 'Неверные учетные данные!'
RE_ENTRY = ''