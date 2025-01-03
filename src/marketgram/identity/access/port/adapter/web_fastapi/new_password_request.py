from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.identity.access.application.new_password_command import (
    NewPasswordCommand, 
    NewPasswordHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


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
    async with RequestContainer(req, res) as container:
        command = NewPasswordCommand(
            token,
            field.new_password,
        )
        handler = await container.get(NewPasswordHandler)
        await handler.handle(command)

        res.delete_cookie('s_id')

        return 'OK'