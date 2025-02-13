from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserCreationCommand:
    email: str
    password: str


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str
    device: str


@dataclass
class ChangePasswordCommand:
    session_id: UUID
    old_password: str
    new_password: str


@dataclass
class SetNewPasswordCommand:
    token: str
    password: str