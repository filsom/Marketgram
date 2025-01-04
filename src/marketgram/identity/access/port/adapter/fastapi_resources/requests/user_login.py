from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.application.handler import Handler
from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.user_login import (
    UserLoginCommand, 
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


class UserLoginField(BaseModel):
    email: str
    password: str


@router.post('/login')
async def user_login_controller(
    field: UserLoginField, 
    req: Request, 
    res: Response
) -> str:
    async with Container(req) as container:
        command = UserLoginCommand(
            field.email,
            field.password,
            req.headers.get('user-agent'),
        )
        handler = await container.get(
            Handler[UserLoginCommand, dict[str, str]]
        )
        result = await handler.handle(command)

        res.set_cookie(
            's_id',
            result['session_id'],
            expires=result['expires_in'],
            httponly=True
        )
        return 'OK'