from fastapi import HTTPException, Request, Response, status
from pydantic import BaseModel

from marketgram.common.port.adapter.container import RequestContainer
from marketgram.identity.access.application.commands.change_password import (
    ChangePasswordCommand, 
    ChangePasswordHandler
)
from marketgram.identity.access.port.adapter.web_fastapi.routing import router


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    same_new_password: str


@router.post('/change_pwd')
async def change_password_controller(
    field: ChangePasswordRequest,
    req: Request,
    res: Response,
) -> str:
    async with RequestContainer(req, res) as container:
        session_id = req.cookies.get('s_id')
        if session_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        command = ChangePasswordCommand(
            session_id,
            field.old_password,
            field.new_password,
            field.same_new_password
        )
        handler = await container.get(ChangePasswordHandler)
        await handler.handle(command)

        res.delete_cookie('s_id')

        return 'OK'