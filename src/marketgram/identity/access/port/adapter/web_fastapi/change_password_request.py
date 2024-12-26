from fastapi import Request, Response
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.identity.access.application.change_password_command import (
    ChangePasswordCommand, 
    ChangePasswordHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    same_new_password: str


@router.post('/change_pwd')
async def change_password(
    field: ChangePasswordRequest,
    req: Request,
    res: Response,
) -> str:
    async with RequestContainer(req, res) as container:
        command = ChangePasswordCommand(
            field.old_password,
            field.new_password
        )
        handler = await container.get(ChangePasswordHandler)
        await handler.handle(command)

        res.delete_cookie('s_id')

        return 'OK'