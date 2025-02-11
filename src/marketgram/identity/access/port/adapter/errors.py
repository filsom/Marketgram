class InfrastructureError(Exception):
    pass


class  JwtVerifyError(InfrastructureError):
    pass

JWT_ERROR = 'Некорректный токен'