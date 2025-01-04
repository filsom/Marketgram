from fastapi import HTTPException, Request, Response, status
from pydantic import BaseModel

from marketgram.common.port.adapter.container import Container
from marketgram.identity.access.application.commands.password_change import (
    PasswordChangeCommand, 
    PasswordChangeHandler
)
from marketgram.identity.access.port.adapter.fastapi_resources.routing import router


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
    async with Container(req) as container:
        session_id = req.cookies.get('s_id')
        if session_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        command = PasswordChangeCommand(
            session_id,
            field.old_password,
            field.new_password,
            field.same_new_password
        )
        handler = await container.get(PasswordChangeHandler)
        await handler.handle(command)
        
        res.delete_cookie('s_id')

        return 'OK'