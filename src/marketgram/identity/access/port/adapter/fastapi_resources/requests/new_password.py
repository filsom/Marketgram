from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.application.handler import Handler
from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.new_password import (
    NewPasswordCommand, 
    NewPassword
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


class NewPasswordField(BaseModel):
    new_password: str
    same_new_password: str


@router.put('/new_pwd/{token}')
async def new_password_controller(
    token: str,
    field: NewPasswordField,
    req: Request,
    res: Response
) -> str:
    async with Container(req) as container:
        command = NewPasswordCommand(
            token,
            field.new_password,
            field.same_new_password
        )
        handler = await container.get(
            Handler[NewPasswordCommand, None]
        )
        await handler.handle(command)

        res.delete_cookie('s_id')

        return 'OK'