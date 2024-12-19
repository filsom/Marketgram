from pydantic import BaseModel


class UserRegistrationField(BaseModel):
    email: str
    password: str
    same_password: str


class UserLoginField(BaseModel):
    email: str
    password: str


class ChangePasswordField(BaseModel):
    old_password: str
    new_password: str
    same_new_password: str


class NewPasswordField(BaseModel):
    new_password: str
    same_new_password: str
