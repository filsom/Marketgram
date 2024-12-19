class DomainException(Exception):
    pass

USER_ACTIVATED = 'Пользователь подтвердил свой Email адрес.' 
USER_NOT_ACTIVATED = 'Пользователь не подтвердил свой Email адрес.'


class PasswordException(DomainException):
    pass

INVALID_EMAIL_OR_PASSWORD = 'Неверный Email или пароль!'
INVALID_PASSWORD = 'Неверный пароль!'
OLD_PASSWORD_SAME = 'Новый пароль совпадает со старым.'