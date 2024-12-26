from fastapi import APIRouter, Request, Response

from marketgram.identity.access.application.change_password_command import (
    ChangePasswordCommand, 
    ChangePasswordHandler
)
from marketgram.identity.access.application.forgot_password_coomand import (
    ForgotPasswordCommand, 
    ForgotPasswordHandler
)
from marketgram.identity.access.application.new_password_command import (
    NewPasswordCommand, 
    NewPasswordHandler
)
from marketgram.identity.access.application.user_activate_command import (
    UserAcivateCommand, 
    UserActivateHandler
)
from marketgram.identity.access.application.user_login_command import (
    UserLoginCommand, 
    UserLoginHandler
)
from marketgram.identity.access.application.user_registration_command import (
    UserRegistrationCommand, 
    UserRegistrationHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.input_data import (
    ChangePasswordField, 
    NewPasswordField, 
    UserLoginField, 
    UserRegistrationField
)
from marketgram.identity.access.port.adapter.web_fastapi.input_data_validators import (
    user_email_validator, 
    user_password_validator, 
    user_registration_cmd_validator
)
from marketgram.identity.access.port.adapter.web_fastapi.container import (
    Container, 
    RequestContainer
)


router = APIRouter(
    prefix='/identity',
    tags=['Identity, Access'],
)


@router.post('/registration')
async def user_registration(field: UserRegistrationField, request: Request):
    async with Container(request) as container:
        user_registration_cmd_validator(
            field.email,
            field.password,
            field.same_password
        )
        handler: UserRegistrationHandler = await container.get(
            UserRegistrationHandler
        )
        await handler.handle(UserRegistrationCommand(
            field.email,
            field.password,
            field.same_password
        ))
        return 'OK'


@router.post('/login')
async def user_login(field: UserLoginField, request: Request, response: Response):
    async with RequestContainer(request, response) as container:
        handler: UserLoginHandler = await container.get(
            UserLoginHandler
        )
        result = await handler.handle(UserLoginCommand(
            field.email,
            field.password,
            request.headers.get('user-agent'),
        ))
        response.set_cookie(
            's_id',
            result['session_id'],
            expires=result['expires_in'],
            httponly=True
        )
        return 'OK'


@router.get('/activate/{token}')
async def activate(token: str, request: Request):
    async with Container(request) as container:
        handler: UserActivateHandler = await container.get(
            UserActivateHandler
        )
        await handler.handle(UserAcivateCommand(token))

        return 'OK'


@router.post('/change_pwd')
async def activate(
    field: ChangePasswordField,
    request: Request,
    response: Response,
):
    async with RequestContainer(request, response) as container:
        user_password_validator(
            field.new_password,
            field.same_new_password
        )
        handler: ChangePasswordHandler = await container.get(
            ChangePasswordHandler
        )
        await handler.handle(ChangePasswordCommand(
            field.old_password,
            field.new_password
        ))
        response.delete_cookie('s_id')

        return 'OK'
    

@router.post('/forgot_pwd')
async def activate(email: str, request: Request, response: Response):
    async with RequestContainer(request, response) as container:
        user_email_validator(email)

        handler: ForgotPasswordHandler = await container.get(
            ForgotPasswordHandler
        )
        await handler.handle(ForgotPasswordCommand(email))

        return 'OK'
    

@router.put('/new_pwd/{token}')
async def activate(
    token: str,
    field: NewPasswordField,
    request: Request,
    response: Response
):
    async with RequestContainer(request, response) as container:
        user_password_validator(
            field.new_password,
            field.same_new_password
        )
        handler: NewPasswordHandler = await container.get(
            NewPasswordHandler
        )
        await handler.handle(NewPasswordCommand(
            token,
            field.new_password,
        ))
        response.delete_cookie('s_id')

        return 'OK'