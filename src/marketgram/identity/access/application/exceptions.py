class ApplicationException(Exception):
    pass


class IncorrectDataFormat(ApplicationException):
    pass

ENTERED_PASSWORD_DO_NOT_MATCH = 'Введенные пароли не совпадают!'
ENTERED_PASSWORD_IS_INCORRECT = 'Введенный пароль имеет некорректное значение!'
ENTERED_EMAIL_IS_INCORRECT = 'Введенный Email имеет некорректное значение!'

