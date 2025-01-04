from .routing import router

from ..fastapi_resources.requests.change_password import change_password_controller
from ..fastapi_resources.requests.forgot_password import forgot_password_controller
from ..fastapi_resources.requests.get_user import get_user_controller
from ..fastapi_resources.requests.new_password import new_password_controller
from ..fastapi_resources.requests.user_activate import user_activate_controller
from ..fastapi_resources.requests.user_login import user_login_controller
from ..fastapi_resources.requests.user_registration import user_registration_controller


__all__ = [
    'router'
]
