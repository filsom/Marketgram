from email_validator import EmailNotValidError, validate_email

from marketgram.identity.access.application.exceptions import (
    ENTERED_EMAIL_IS_INCORRECT, 
    ENTERED_PASSWORD_DO_NOT_MATCH, 
    ENTERED_PASSWORD_IS_INCORRECT, 
    IncorrectDataFormat
)


def user_email_validator(email: str) -> None:
    try:
        validate_email(email)
    except EmailNotValidError:
        raise IncorrectDataFormat(ENTERED_EMAIL_IS_INCORRECT)
    

def user_password_validator(password: str, same_password: str) -> None:
    if password != same_password:
        raise IncorrectDataFormat(ENTERED_PASSWORD_DO_NOT_MATCH)
    
    if len(password) < 8:
        raise IncorrectDataFormat(ENTERED_PASSWORD_IS_INCORRECT)
    
    for x in password:
        if x.isspace():
            raise IncorrectDataFormat(ENTERED_PASSWORD_IS_INCORRECT)


def user_registration_cmd_validator(
    email: str, 
    password: str, 
    same_password: str
) -> None:
    user_email_validator(email)
    user_password_validator(password, same_password)