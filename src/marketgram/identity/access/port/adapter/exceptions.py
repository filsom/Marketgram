class InfrastructureException(Exception):
    pass


class AnalysisErrorHMAC(InfrastructureException):
    pass

UNKNOWN_VALUE = 'Неизвестное значение'


class Unauthorized(InfrastructureException):
    pass

ACCESS_DENIED = 'Требуется авторизация. Пожалуйста, войдите в свою учетную запись!'


class  JWTVerifyException(InfrastructureException):
    pass

JWT_ERROR = 'Некорректный токен'


class UnknowException(Exception):
    pass

UNKNOWN_EXCEPTION = 'Возникла неизвестная ошибка. Повторите операцию позже!'